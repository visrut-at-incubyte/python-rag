const x = {
    type: 'session.update',
    session: {
      turn_detection: { type: 'server_vad' },
      instructions: 'You are an AI assistant that helps people find information. Say Hello at the start of the call. And ask for the name of the person speaking. After that ask them how you can help them',
      voice: 'shimmer',
      input_audio_format: 'pcm16',
      output_audio_format: 'pcm16',
      input_audio_transcription: { model: 'whisper-1' },
      tool_choice: 'auto',
      tools: [
        {
          type: 'function',
          name: 'referToMedicalDatabase',
          desciption: 'You can call this function to get the refer to medical database when asked for appointment, prescription or lab results.',
          parameters: {
            type: 'object',
            properties: {
              user_query: {
                type: 'string',
                description: 'User query to refer to medical database'
              }
            },
            required: [ 'user_query' ],
            additionalProperties: false
          }
        }
      ]
    }
  }