// set OPENAI_API_KEY, purchase API Credits
// update node
// python.exe -m pip install --upgrade pip
// npm install openai (not pip)
// node example.mjs (module js, or ESM: ECMAScript module system)

import OpenAI from 'openai'
const openaiClient = new OpenAI()

const modelVal = 'gpt-5'
const inputVal = [
	'Explain oxidase in simple terms.',
	'Describe the purpose of each complex in the Electron Transport Chain.',
	'Write a 4 sentence description of the Electron Transport Chain.',
	'Write a one sentence story about Batman.'
]

const response = await openaiClient.responses.create({
  model: modelVal,
  input: inputVal[0],
})

console.log(response.output_text)
