# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import os

from google.adk.tools.tool_context import ToolContext

logger = logging.getLogger(__name__)


def get_hotels(location: str,  tool_context: ToolContext, count: int = 5) -> str:
    """Call this tool to get a list of hotels based on location.
    'count' is the number of hotels to return.
    """
    logger.info(f"--- TOOL CALLED: get_hotels (count: {count}) ---")
    # logger.info(f"  - Cuisine: {cuisine}")
    logger.info(f"  - Location: {location}")

    items = []
    if "new york" in location.lower() or "ny" in location.lower():
        try:
            script_dir = os.path.dirname(__file__)
            file_path = os.path.join(script_dir, "hotel_data.json")
            with open(file_path) as f:
                hotel_data_str = f.read()
                if base_url := tool_context.state.get("base_url"):                    
                    hotel_data_str = hotel_data_str.replace("http://localhost:10002", base_url)
                    logger.info(f'Updated base URL from tool context: {base_url}')
                all_items = json.loads(hotel_data_str)        

            # Slice the list to return only the requested number of items
            items = all_items[:count]
            logger.info(
                f"  - Success: Found {len(all_items)} hotels, returning {len(items)}."
            )

        except FileNotFoundError:
            logger.error(f"  - Error: hotel_data.json not found at {file_path}")
        except json.JSONDecodeError:
            logger.error(f"  - Error: Failed to decode JSON from {file_path}")

    return json.dumps(items)
