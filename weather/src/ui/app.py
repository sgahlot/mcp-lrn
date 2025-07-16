#!/usr/bin/env python3
"""
Simple Streamlit Client for Weather MCP Server
Based on working CLI client approach
"""

import asyncio
import os
import streamlit as st
from fastmcp import Client


class WeatherMCPClient:
    """Simple MCP client wrapper using fastmcp"""
    
    def __init__(self):
        self.connected = False
        self.tools = []
        self.resources = []
        self.resource_templates = []
    
    async def connect_and_get_info(self, api_key: str):
        """Connect to server and get tools/resources using fastmcp"""
        # Set environment variable for the server
        os.environ["WEATHER_API_KEY"] = api_key
        
        # Use same approach as CLI client - relative path to server
        async with Client("../../server.py") as client:
            # Get resources with detailed info
            resources = await client.list_resources()
            self.resources = []
            for resource in resources:
                self.resources.append({
                    "name": getattr(resource, 'name', 'Unknown'),
                    "uri": getattr(resource, 'uri', 'Unknown'),
                    "description": getattr(resource, 'description', 'No description'),
                    "mimeType": getattr(resource, 'mimeType', 'Unknown'),
                    "full_str": str(resource)
                })
            
            # Get resource templates with detailed info
            resource_templates = await client.list_resource_templates()
            self.resource_templates = []
            for template in resource_templates:
                self.resource_templates.append({
                    "name": getattr(template, 'name', 'Unknown'),
                    "uriTemplate": getattr(template, 'uriTemplate', 'Unknown'),
                    "description": getattr(template, 'description', 'No description'),
                    "mimeType": getattr(template, 'mimeType', 'Unknown'),
                    "full_str": str(template)
                })
            
            # Get tools with detailed info
            tools = await client.list_tools()
            self.tools = []
            for tool in tools:
                self.tools.append({
                    "name": getattr(tool, 'name', 'Unknown'),
                    "description": getattr(tool, 'description', 'No description'),
                    "inputSchema": getattr(tool, 'inputSchema', {}),
                    "full_str": str(tool)
                })
        
        self.connected = True
        return True
    
    def disconnect(self):
        """Disconnect from server"""
        self.connected = False
        self.tools = []
        self.resources = []
        self.resource_templates = []


def run_async(coro):
    """Run async function"""
    try:
        return asyncio.run(coro)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()


def main():
    """Main Streamlit app"""
    st.set_page_config(page_title="Weather MCP Client", page_icon="🌤️")
    st.title("🌤️ Weather MCP Client")
    
    # Initialize client
    if "mcp_client" not in st.session_state:
        st.session_state.mcp_client = WeatherMCPClient()
    
    # Connection section
    st.header("🔌 Connection")
    
    api_key = st.text_input(
        "Weather API Key", 
        type="password",
        value=os.getenv("WEATHER_API_KEY", ""),
        help="Enter your WeatherAPI.com API key"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Connect", type="primary"):
            if api_key:
                try:
                    with st.spinner("Connecting to server..."):
                        success = run_async(st.session_state.mcp_client.connect_and_get_info(api_key))
                        if success:
                            st.success("✅ Connected!")
                            st.rerun()
                except Exception as e:
                    st.error(f"❌ Connection failed: {e}")
            else:
                st.error("Please enter an API key")
    
    with col2:
        if st.button("Disconnect"):
            st.session_state.mcp_client.disconnect()
            st.info("🔌 Disconnected")
            st.rerun()
    
    # Status
    st.header("📊 Status")
    if st.session_state.mcp_client.connected:
        st.success("🟢 **Connected** to Weather MCP Server")
    else:
        st.error("🔴 **Not Connected** to Weather MCP Server")
    
    # Display results when connected
    if st.session_state.mcp_client.connected:
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔧 Tools", len(st.session_state.mcp_client.tools))
        with col2:
            st.metric("📚 Resources", len(st.session_state.mcp_client.resources))
        with col3:
            st.metric("📄 Templates", len(st.session_state.mcp_client.resource_templates))
        
        st.divider()
        
        # Tools section with enhanced formatting
        st.header("🔧 Available Tools")
        if st.session_state.mcp_client.tools:
            for i, tool in enumerate(st.session_state.mcp_client.tools, 1):
                with st.expander(f"🛠️ {tool['name']}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**Description:** {tool['description']}")
                        if tool['inputSchema']:
                            st.write("**Input Schema:**")
                            st.json(tool['inputSchema'])
                    with col2:
                        st.info(f"Tool #{i}")
                        if st.button(f"Show Raw", key=f"tool_raw_{i}"):
                            st.code(tool['full_str'], language="text")
        else:
            st.warning("No tools found")
        
        st.divider()
        
        # Resources section with enhanced formatting
        st.header("📚 Available Resources")
        if st.session_state.mcp_client.resources:
            for i, resource in enumerate(st.session_state.mcp_client.resources, 1):
                with st.expander(f"📄 {resource['name']}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**URI:** `{resource['uri']}`")
                        st.write(f"**Description:** {resource['description']}")
                        st.write(f"**MIME Type:** `{resource['mimeType']}`")
                    with col2:
                        st.info(f"Resource #{i}")
                        if st.button(f"Show Raw", key=f"resource_raw_{i}"):
                            st.code(resource['full_str'], language="text")
        else:
            st.warning("No resources found")
        
        # Resource Templates section with enhanced formatting
        if st.session_state.mcp_client.resource_templates:
            st.divider()
            st.header("📄 Resource Templates")
            for i, template in enumerate(st.session_state.mcp_client.resource_templates, 1):
                with st.expander(f"📋 {template['name']}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**URI Template:** `{template['uriTemplate']}`")
                        st.write(f"**Description:** {template['description']}")
                        st.write(f"**MIME Type:** `{template['mimeType']}`")
                    with col2:
                        st.info(f"Template #{i}")
                        if st.button(f"Show Raw", key=f"template_raw_{i}"):
                            st.code(template['full_str'], language="text")


if __name__ == "__main__":
    main() 