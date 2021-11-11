# ============================================================================
# FILE: database.py
# AUTHOR: Elonia Moonbeam
# License: MIT license
# ============================================================================
from deoplete.base.source import Base
from deoplete.util import Candidates, UserContext
from pynvim import Nvim

import database_editor
import latex_parser

class Source(Base):
	def __init__(self, vim: Nvim) -> None:
		super().__init__(vim)
		self.name = 'database'
		self.mark = '[D]'
		self.rank = 500
		self.min_pattern_length = 0  # start matching without anything typed
		# self.filetypes = ["tex"]

	def str_to_candidate(self, words):
		return [{'word': word} for word in words]

	def gather_candidates(self, context: UserContext) -> Candidates:
		syntax_elements = self.vim.call("synstack", context["position"][1], max(context["position"][2] - 1, 1))
		syntax_names = self.vim.call("map", syntax_elements, 'synIDattr(v:val, "name")')
		deoplete.util.debug(self.vim, syntax_names)
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
