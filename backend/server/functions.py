# TODO: Delete this file, probably.

import json

from backend.shared.enums import MessageType


def create_dumped_message(msg_type: MessageType, payload: dict) -> str:
	msg = {
		"type": msg_type.value,
		**payload
	}

	return json.dumps(msg)
