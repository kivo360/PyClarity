from pyclarity.server.mcp_server import create_server

app = create_server()


if __name__ == "__main__":
    app.run(transport="http", host="0.0.0.0", port=9020)
