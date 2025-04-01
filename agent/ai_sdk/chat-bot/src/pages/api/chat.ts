// import { OpenAI } from '@ai-sdk/openai';
// import { OpenAI } from 'openai';
// const openai = new OpenAI({
//   apiKey: process.env.OPENAI_API_KEY!,
// });

// import { NextApiRequest, NextApiResponse } from 'next';

// export default async function handler(req: NextApiRequest, res: NextApiResponse) {
//   if (req.method !== 'POST') {
//     return res.status(405).json({ error: 'Method not allowed' });
//   }

//   const { messages } = req.body;
//   try {
//     console.log('Received messages:', messages); // Log the received messages
//     const response = await openai.chat.completions.create({
//       model: 'gpt-4o-mini',
//       messages,
//     });
//     console.log('AI response:', response.choices[0].message.content); // Log the AI response
//     res.status(200).json({ message: response.choices[0].message.content });
//   } catch (error) {
//     res.status(500).json({ error: 'Error fetching AI response' });
//   }
// }
export const runtime = 'edge'
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export default async function handler(req: Request) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    const { messages } = await req.json();

    const result = streamText({
      model: openai('gpt-4o'),
      system: 'You are a helpful assistant.',
      messages,
    });

    return result.toDataStreamResponse();
  } catch (error) {
    return new Response(JSON.stringify({ error: 'Error fetching AI response' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}