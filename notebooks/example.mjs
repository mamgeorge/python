// set OPENAI_API_KEY, purchase API Credits
// update node, pip install openai
// node example.mjs

import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
  model: "gpt-5",
  input: "Write a one sentence story about Batman.",
});

console.log(response.output_text);