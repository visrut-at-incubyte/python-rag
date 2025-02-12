# call_handlers.py
import os

from aiohttp import web
from azure.communication.callautomation import CallAutomationClient


class CallHandler:
    def __init__(self):
        connection_string = os.getenv("CONNECTION_STRING")
        self.acs_client = CallAutomationClient.from_connection_string(connection_string)

    async def handle_incoming_call(self, request):
        try:
            events = await request.json()
            event = events[0]
            
            if event["eventType"] == "Microsoft.EventGrid.SubscriptionValidationEvent":
                print("Received SubscriptionValidation event")
                return web.json_response({
                    "validationResponse": event["data"]["validationCode"]
                })

            event_data = event["data"]
            caller_id = event_data["from"]["rawId"]
            callback_uri = f"{os.getenv('CALLBACK_URI')}/api/callbacks/{caller_id}"

            # Create answer call options
            answer_call_options = {
                "cognitive_services_endpoint": os.getenv("COGNITIVE_SERVICES_ENDPOINT"),
                "media_streaming": {
                    "type": "websocket",
                    "content_type": "audio",
                    "audio_channel_type": "unmixed",
                    "start_media_streaming": True,
                    "enable_bidirectional": True,
                    "audio_format": "Pcm24KMono"
                }
            }

            answer_call_result = await self.acs_client.answer_call(
                incoming_call_context=event_data["incomingCallContext"],
                callback_url=callback_uri,
                **answer_call_options
            )

            print(f"Answer call ConnectionId: {answer_call_result.call_connection_id}")
            return web.Response(status=200)

        except Exception as e:
            print(f"Error during the incoming call event: {str(e)}")
            return web.Response(status=500)

    async def handle_callbacks(self, request):
        try:
            events = await request.json()
            event = events[0]
            event_data = event["data"]
            call_connection_id = event_data["callConnectionId"]
            
            print(f"Received Event: {event['type']}, CallConnectionId: {call_connection_id}")

            if event["type"] == "Microsoft.Communication.CallConnected":
                call_connection = self.acs_client.get_call_connection(call_connection_id)
                properties = await call_connection.get_properties()
                print(f"Call properties: {properties}")

            elif event["type"] == "Microsoft.Communication.MediaStreamingStarted":
                print(f"Media streaming started: {event_data}")

            elif event["type"] == "Microsoft.Communication.MediaStreamingStopped":
                print(f"Media streaming stopped: {event_data}")

            elif event["type"] == "Microsoft.Communication.MediaStreamingFailed":
                print(f"Media streaming failed: {event_data}")

            elif event["type"] == "Microsoft.Communication.CallDisconnected":
                print(f"Call disconnected: {event_data}")

            return web.Response(status=200)

        except Exception as e:
            print(f"Error handling callback: {str(e)}")
            return web.Response(status=500)
