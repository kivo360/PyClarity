#!/usr/bin/env python3
"""
Test database connectivity for PyClarity
"""

import asyncio

import asyncpg

from pyclarity.config import MCPConfig


async def test_database_connection():
    """Test PostgreSQL connection"""
    print("🧪 Testing Database Connectivity")
    print("=" * 40)

    # Load configuration
    config = MCPConfig()
    db_url = config.database_url

    print(f"📋 Database URL: {db_url}")

    try:
        # Test connection
        conn = await asyncpg.connect(db_url)
        print("✅ Database connection successful!")

        # Test basic query
        result = await conn.fetchval("SELECT version()")
        print(f"📊 PostgreSQL version: {result}")

        # Test if we can create a table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        print("✅ Table creation successful!")

        # Test insert
        await conn.execute(
            """
            INSERT INTO test_table (name) VALUES ($1)
        """,
            "test_record",
        )
        print("✅ Insert operation successful!")

        # Test select
        rows = await conn.fetch("SELECT * FROM test_table")
        print(f"✅ Select operation successful! Found {len(rows)} rows")

        # Clean up
        await conn.execute("DROP TABLE IF EXISTS test_table")
        print("✅ Cleanup successful!")

        await conn.close()
        print("\n🎉 All database operations successful!")

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

    return True


async def test_mcp_server_with_db():
    """Test MCP server with database integration"""
    print("\n🧪 Testing MCP Server with Database")
    print("=" * 40)

    from pyclarity.config import MCPConfig
    from pyclarity.server.mcp_server import PyClarityMCPServer

    config = MCPConfig()
    server = PyClarityMCPServer(config)

    print("✅ MCP Server created with database config")
    print(f"📋 Database URL: {config.database_url}")
    print(f"🔧 Auth enabled: {config.auth.enabled}")
    print(f"🌐 Server host: {config.server.host}")
    print(f"🔌 Server port: {config.server.port}")

    # Test server start
    await server.start(host=config.server.host, port=config.server.port)

    print("\n✅ MCP Server with database integration test completed!")


async def main():
    """Main test function"""
    print("🚀 PyClarity Database & MCP Server Test")
    print("=" * 50)

    # Test database connectivity
    db_success = await test_database_connection()

    if db_success:
        # Test MCP server with database
        await test_mcp_server_with_db()
    else:
        print("❌ Skipping MCP server test due to database failure")


if __name__ == "__main__":
    asyncio.run(main())
