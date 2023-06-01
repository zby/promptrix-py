import unittest
from promptrixTypes import *
from PromptSectionBase import PromptSectionBase
from VolatileMemory import VolatileMemory
from FunctionRegistry import FunctionRegistry
from GPT3Tokenizer import GPT3Tokenizer

class TestSection(PromptSectionBase):
    async def render_as_messages(self, memory: PromptMemory, functions: PromptFunctions, tokenizer: Tokenizer, max_tokens: int):
        return self.return_messages([{'role': 'test', 'content': 'Hello Big World'}], 3, tokenizer, max_tokens)


class MultiTestSection(PromptSectionBase):
    async def render_as_messages(self, memory: PromptMemory, functions: PromptFunctions, tokenizer: Tokenizer, max_tokens: int):
        return self.return_messages([{'role': 'test', 'content': 'Hello Big'}, {'role': 'test', 'content': 'World'}], 3, tokenizer, max_tokens)

class TestPromptSectionBase(unittest.TestCase):
    def setUp(self):
        self.memory = VolatileMemory()
        self.functions = FunctionRegistry()
        self.tokenizer = GPT3Tokenizer()

    def test_constructor(self):
        section = TestSection()
        self.assertEqual(section.tokens, -1)
        self.assertEqual(section.required, True)
        self.assertEqual(section.separator, "\n")
        self.assertEqual(section.text_prefix, "")

    async def test_render_as_messages(self):
        section = TestSection()
        rendered = await section.render_as_messages(self.memory, self.functions, self.tokenizer, 100)
        self.assertEqual(rendered['output'], [{'role': 'test', 'content': 'Hello Big World'}])
        self.assertEqual(rendered['length'], 3)
        self.assertEqual(rendered['tooLong'], False)

        section = TestSection(2)
        rendered = await section.render_as_messages(self.memory, self.functions, self.tokenizer, 100)
        self.assertEqual(rendered['output'], [{'role': 'test', 'content': 'Hello Big'}])
        self.assertEqual(rendered['length'], 2)
        self.assertEqual(rendered['tooLong'], False)

        section = TestSection(2)
        rendered = await section.render_as_messages(self.memory, self.functions, self.tokenizer, 1)
        self.assertEqual(rendered['output'], [{'role': 'test', 'content': 'Hello Big'}])
        self.assertEqual(rendered['length'], 2)
        self.assertEqual(rendered['tooLong'], True)

        section = MultiTestSection(2)
        rendered = await section.render_as_messages(self.memory, self.functions, self.tokenizer, 100)
        self.assertEqual(rendered['output'], [{'role': 'test', 'content': 'Hello Big'}])
        self.assertEqual(rendered['length'], 2)
        self.assertEqual(rendered['tooLong'], False)

    async def test_render_as_text(self):
        section = TestSection()
        rendered = await section.render_as_text(self.memory, self.functions, self.tokenizer, 100)
        self.assertEqual(rendered['output'], "Hello Big World")
        self.assertEqual(rendered['length'], 3)
        self.assertEqual(rendered['tooLong'], False)

        section = TestSection(4, True, "\n", "user: ")
        rendered = await section.render_as_text(self.memory, self.functions, self.tokenizer, 100)
        self.assertEqual(rendered['output'], "user: Hello Big")
        self.assertEqual(rendered['length'], 4)
        self.assertEqual(rendered['tooLong'], False)

        section = TestSection(4, True, "\n", "user: ")
        rendered = await section.render_as_text(self.memory, self.functions, self.tokenizer, 1)
        self.assertEqual(rendered['output'], "user: Hello Big")
        self.assertEqual(rendered['length'], 4)
        self.assertEqual(rendered['tooLong'], True)


if __name__ == '__main__':
    unittest.main()
