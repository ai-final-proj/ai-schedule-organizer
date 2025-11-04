# Debugging Empty AI Responses

## Changes Made

I've added extensive logging to help debug the empty response issue:

### Frontend Changes (`chat-screen.component.ts`)
- Added console logging for response status, data, and final reply
- Implemented robust recursive text extraction that handles ANY n8n response format:
  - Direct string responses
  - Objects with common text fields: `description`, `text`, `message`, `output`, `response`, `result`, `content`, `body`, `data`
  - Nested arrays (extracts and joins all text content)
  - Complex nested objects (recursively searches for text)
  - Fallback to pretty-printed JSON for unknown formats
- Added detection for empty responses with helpful error message
- Simplified code using `extractTextFromResponse()` utility function

### Backend Changes (`prompt.py`)
- Added debug logging for:
  - n8n URL and payload being sent
  - n8n response status code
  - n8n response text (first 500 chars)
  - Parsed JSON response
  - Final result being returned to frontend

## How to Test

### 1. Rebuild the Docker Container

```bash
cd ~/app
docker rm -f ai_schedule_container
docker build -t ai-schedule-organizer .
docker run -d --name ai_schedule_container \
  -p 7860:7860 \
  -e DATABASE_URL="postgresql+psycopg://neondb_owner:npg_MPZ3lB5RtSve@ep-green-truth-adedoaj5-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" \
  -e SECRET_KEY=dev \
  -e PORT=7860 \
  ai-schedule-organizer:latest
```

### 2. Monitor Logs

```bash
docker logs -f ai_schedule_container
```

### 3. Test the Chat

1. Open the chat interface in your browser
2. Open browser DevTools (F12) and go to Console tab
3. Send a test message
4. Look for console logs showing:
   - `Response status: 200`
   - `Response data: {...}`
   - `Final reply: ...`

### 4. Check Backend Logs

In the Docker logs, you should now see:
```
[DEBUG] Sending to n8n: http://35.224.46.46:5678/webhook/...
[DEBUG] Payload: [{'sessionId': '...', 'action': 'sendMessage', 'chatInput': '...'}]
[DEBUG] n8n status code: 200
[DEBUG] n8n response text (first 500 chars): ...
[DEBUG] Parsed n8n JSON response: {...}
[DEBUG] Returning to frontend: {...}
```

## Common Issues to Check

### 1. n8n Webhook Not Responding
- Check if n8n instance at `http://35.224.46.46:5678` is running
- Verify the webhook URL is correct: `/webhook/e0991a38-144d-4fb6-a2c9-98cd9de23988`
- Check n8n logs for errors

### 2. n8n Returning Empty Response
- The debug logs will show exactly what n8n returns
- Check if n8n workflow is properly configured to return data

### 3. Session ID Issues
- Check browser console for "Restored session: ..." or "Created new session: ..."
- The sessionId is now persisted in localStorage
- To reset: Open browser console and run: `localStorage.removeItem('chatSessionId')`

### 4. Response Format Issues
- The code now handles multiple response formats
- If n8n returns a format we don't handle, it will be stringified and shown
- Check the console logs to see the exact format

## Response Formats Now Handled

The new `extractTextFromResponse()` function can handle ANY of these n8n response formats:

### Format 1: Simple String
```json
{"n8n_response": "Hello, how can I help?"}
```
**Result:** "Hello, how can I help?"

### Format 2: Object with text field
```json
{"n8n_response": {"text": "Your answer here"}}
```
**Result:** "Your answer here"

### Format 3: Array of objects with descriptions (your current format)
```json
{
  "n8n_response": {
    "text": [
      {"task_index": 0, "description": "First task completed"},
      {"task_index": 1, "description": "Second task completed"}
    ]
  }
}
```
**Result:**
```
First task completed

Second task completed
```

### Format 4: Direct array
```json
{"n8n_response": ["Item 1", "Item 2", "Item 3"]}
```
**Result:**
```
Item 1

Item 2

Item 3
```

### Format 5: Nested objects
```json
{
  "n8n_response": {
    "result": {
      "message": "Operation successful"
    }
  }
}
```
**Result:** "Operation successful"

### Format 6: Multiple text fields (tries in priority order)
```json
{
  "n8n_response": {
    "output": "This will be shown",
    "text": "This won't (lower priority)"
  }
}
```
**Result:** "This will be shown"

The function tries these fields in order:
1. `description`
2. `text`
3. `message`
4. `output`
5. `response`
6. `result`
7. `content`
8. `body`
9. `data`

If none are found, it pretty-prints the JSON.

## Quick Debug Commands

### View sessionId in browser console:
```javascript
localStorage.getItem('chatSessionId')
```

### Reset session:
```javascript
localStorage.removeItem('chatSessionId')
location.reload()
```

### Check if frontend is making request:
Look for `POST /api/prompt` in Network tab of DevTools

### Force detailed logging:
The new code logs everything, just check browser console and Docker logs

## What Changed vs Working Version

**Session Management:**
- OLD: `sessionId = uuidv4()` on every page load (new session each time)
- NEW: `sessionId` persisted in localStorage (same session across reloads)

**Issue:** If n8n expects fresh sessions or has issues with persistent sessions, this could cause problems.

**Quick Test:** To test if this is the issue, temporarily use a fresh session:
```javascript
// In browser console:
localStorage.removeItem('chatSessionId')
location.reload()
// Then try sending a message
```

If it works with a fresh session, the issue is with session persistence in n8n.

