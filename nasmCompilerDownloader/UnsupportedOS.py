class UnsupportedOSError(Exception):
    def __init__(self, os_name):
        self.os_name = os_name
        super().__init__(f"Unsupported operating system: {os_name}")

def check_os_supported(os_name):
    supported_os = ['linux', 'macosx', 'win32', 'win64']

    if os_name not in supported_os:
        raise UnsupportedOSError(os_name)