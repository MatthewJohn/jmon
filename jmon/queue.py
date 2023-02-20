
from kombu import Queue, Exchange, binding


from jmon.client_type import ClientType


class QueueGenerator:

    ROUTING_KEY_TO_CLIENT_TYPES_MAPPING = None
    CHECK_EXCHANGE = Exchange('check', type='topic')

    @staticmethod
    def get_routing_key_parts_for_client_types(client_types):
        """Return list of routing key parts from client types"""
        names = [
            client_type.value
            for client_type in client_types
        ]
        names.sort()
        return names

    @classmethod
    def get_routing_key_by_client_types(cls, client_types):
        """Get routing key by client_types"""
        client_type_strings = cls.get_routing_key_parts_for_client_types(client_types)
        return '_'.join(client_type_strings)

    @classmethod
    def get_all_routing_keys_for_client_type(cls, client_type):
        return [
            key
            for key, value in cls.get_routing_key_to_client_types_mapping().items()
            if client_type in value
        ]

    @classmethod
    def get_routing_key_to_client_types_mapping(cls):
        """Get all routing keys"""
        if cls.ROUTING_KEY_TO_CLIENT_TYPES_MAPPING is None:
            remaining_client_types = [
                client_type
                for client_type in ClientType
            ]

            all_keys = {}
            while len(remaining_client_types):
                all_keys[cls.get_routing_key_by_client_types(remaining_client_types)] = list(remaining_client_types)

            cls.ROUTING_KEY_TO_CLIENT_TYPES_MAPPING = all_keys

        print(f'Entire mapping: {cls.ROUTING_KEY_TO_CLIENT_TYPES_MAPPING}')
        return cls.ROUTING_KEY_TO_CLIENT_TYPES_MAPPING
