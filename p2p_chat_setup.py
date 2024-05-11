from cx_Freeze import setup, Executable

setup(
    name="p2p chat",
    version="0.1.0",
    description="Chat for 1 - 5 people with local sockets",
    executables=[Executable("p2p_chat.py")]
)
