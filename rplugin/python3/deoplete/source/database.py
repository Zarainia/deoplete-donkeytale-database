# ============================================================================
# FILE: database.py
# AUTHOR: Elonia Moonbeam
# License: MIT license
# ============================================================================
import deoplete.util
from pynvim import Nvim
import regex as re
import asyncio
import database_editor
import latex_parser

from deoplete.base.source import Base
from deoplete.util import parse_buffer_pattern, getlines
from deoplete.util import UserContext, Candidates

class Source(Base):
	def __init__(self, vim: Nvim) -> None:
		super().__init__(vim)
		self.name = 'database'
		self.mark = '[D]'
		self.rank = 500
		self.vars = {
			'range_above': 20,
			'range_below': 20,
			'max_line_length': 100
		}
		self.min_pattern_length = 0
		custom_vars = self.vim.call(
				'deoplete#custom#_get_source_vars', self.name
		)
		if custom_vars:
			self.vars.update(custom_vars)
		self.vim.vars["database_completion_results"] = []
		self.vim.vars["database_completion_calculating"] = 0
		self.result = []

	def _get_event_argument_number(self, text):
		search_string = "event"
		ind = text.rfind(search_string) + len(search_string)
		groups = 0
		balance = 0
		for char in text[ind:]:
			match char:
				case '{':
					balance += 1
				case '}':
					balance -= 1
					if balance == 0:
						groups += 1
		return groups, balance

	def gather_candidates(self, context: UserContext) -> Candidates:
		syntax_elements = self.vim.call("synstack", context["position"][1], max(context["position"][2] - 1, 1))
		syntax_names = self.vim.call("map", syntax_elements, 'synIDattr(v:val, "name")')
		# deoplete.util.debug(self.vim, syntax_names)
		if syntax_names:
			if syntax_names[-1] == "databaseTexEventTypeBase":
				return self.str_to_candidate(database_editor.EVENT_PARTICIPANT_ROLES.keys())
			elif syntax_names[-1] == "databaseTexMultiTraitsNameBase":
				return self.str_to_candidate(latex_parser.TRAIT_NAMES)
			elif syntax_names[-1] == "databaseTexMultiSettingsNameBase":
				return self.str_to_candidate(latex_parser.SETTING_NAMES)
			syntax_parts = syntax_names[-1].split('_')
			if syntax_parts[0] == "databaseTexEvent" and len(syntax_parts) == 3: 
				if syntax_parts[2] == "ParticipantsRoleBase":
					return self.str_to_candidate(database_editor.EVENT_PARTICIPANT_ROLES[syntax_parts[1]])
				elif syntax_parts[2] == "ParticipantsTypeBase":
					return self.str_to_candidate(database_editor.EVENT_PARTICIPANT_TYPES)
		return []
