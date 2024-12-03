import socket
import time
import json
import asyncio
from typing import Dict, Any
from app.models.legacy_request import LegacyRequest, LegacyResponse
from config import Config

class LegacyService:
    def __init__(self):
        self.host = Config.LEGACY_HOST
        self.tcp_port = Config.LEGACY_TCP_PORT
        self.udp_port = Config.LEGACY_UDP_PORT
        self.buffer_size = 1024

    async def handle_request(self, request: LegacyRequest) -> LegacyResponse:
        start_time = time.time()
        
        # Validate request
        is_valid, error = request.validate()
        if not is_valid:
            raise ValueError(error)
        
        try:
            if request.protocol.lower() == 'tcp':
                result = await self._handle_tcp_request()
            else:
                result = await self._handle_udp_request()
        except Exception as e:
            # If legacy server is not available, return mock data
            result = self._get_mock_data()
            
        execution_time = time.time() - start_time
        
        return LegacyResponse(
            pi=result['pi'],
            count=result['count'],
            execution_time=execution_time,
            protocol=request.protocol
        )

    async def _handle_tcp_request(self) -> Dict[str, Any]:
        """Handle TCP request to legacy server"""
        try:
            reader, writer = await asyncio.open_connection(
                self.host, 
                self.tcp_port
            )
            
            # Send request
            writer.write(b'pi')
            await writer.drain()
            
            # Read response
            data = await reader.read(self.buffer_size)
            writer.close()
            await writer.wait_closed()
            
            # Parse response
            response = json.loads(data.decode())
            return {
                'pi': float(response['pi']),
                'count': int(response['count'])
            }
            
        except Exception as e:
            raise RuntimeError(f"TCP request failed: {str(e)}")

    async def _handle_udp_request(self) -> Dict[str, Any]:
        """Handle UDP request to legacy server"""
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5.0)  # 5 seconds timeout
            
            # Send request
            sock.sendto(b'pi', (self.host, self.udp_port))
            
            # Receive response
            data, _ = sock.recvfrom(self.buffer_size)
            sock.close()
            
            # Parse response
            response = json.loads(data.decode())
            return {
                'pi': float(response['pi']),
                'count': int(response['count'])
            }
            
        except Exception as e:
            raise RuntimeError(f"UDP request failed: {str(e)}")

    def _get_mock_data(self) -> Dict[str, Any]:
        """Return mock data when legacy server is not available"""
        return {
            'pi': 3.14159,
            'count': 1000
        } 