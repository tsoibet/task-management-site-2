# task-management-site-2
## Quick start
1. Make sure you are in a correct directory
2. Clone this repo `
git clone https://github.com/tsoibet/task-management-site-2.git
` 
3. Move to the folder `cd task-management-site-2`
3. Start DB and Adminer `docker-compose up -d db adminer`
4. Start flask and nginx `docker-compose up web nginx`
5. Browse to `http://localhost:8080/` to check the sample page

Now you are ready to start!

## Development
### File location
You can edit the files in the `public` folder to create the frontend. Feel free to add/remove/edit any file in `public` folder.

### Workflow
After editing the files in `public` folder, you don't need to restart any docker. Hit the refresh button in the browser and you should see the up-to-date content.

### API
<table>
<tr><th>Endpoint</th><th>Description</th><th>Request</th><th>Respond</th></tr>
<tr>
<td>
<pre>
GET /api/
</pre>
</td>
<td>
Get the health of the Python backend.
</td>
<td>
-
</td>
<td>
If the backend works normally, you will see a JSON object:
<pre>
{
  "server_time": {SERVER_TIME},
  "status": "ok"
}
</pre></td>
</tr>

<tr>
<td>
<pre>
GET /api/status
</pre>
</td>
<td>
Get all the avaliable status for the status field of tasks. 
</td>
<td>
-
</td>
<td>
In JSON array format:
<pre>
[&lt;STATUS_1&gt;,&lt;STATUS_2&gt;,&lt;STATUS_3&gt;]
</pre></td>
</tr>

<tr>
<td>
<pre>
GET /api/tasks?page=&lt;page&gt;&per=&lt;per&gt;&sort=&lt;sort&gt;
</pre>
</td>
<td>
Get all the tasks.
</td>
<td>
Accept query parameters:

<pre>
page:int - To specify the page of result.
per:int - To specify the number of result per page.
sort:string`"status" or "priority" or "deadline"` - To specify the order of the result.
</pre>
</td>
<td>
In JSON object format:
<pre>
{
  "status": "ok",
  "total": &lt;TOTAL_NUMBER_OF_RESULT:int&gt;,
  "tasks": [
    {
      "created_at": &lt;TASK_CREATED_TIME:string`yyyy-mm-ddTHH:mm:ss`&gt;,
      "deadline": &lt;TASK_DEADLINE_TIME:string`yyyy-mm-ddTHH:mm:ss`&gt;,
      "deadlineness": &lt;HAVE_DEADLINE_INDICATOR:boolean&gt;,
      "detail": &lt;TASK_DETAIL:string&gt;,
      "id": &lt;TASK_ID:int&gt;,
      "priority": &lt;TASK_PRIORITY:int&gt;,
      "status": &lt;TASK_STATUS:ref`/status/`&gt;,
      "title": &lt;TASK_TITLE:string&gt;
    },
    {...
  ]
}
</pre></td>
</tr>

<tr>
<td>
<pre>
GET /api/task/&lt;id&gt;
</pre>
</td>
<td>
Get a specific task. A specific task of the provided id will be returned.
</td>
<td>
Accept path parameters:

<pre>
id:int - To specify the id of task.
</pre>
</td>
<td>
In JSON object format:
<pre>
{
  "status": "ok",
  "tasks": {
    "created_at": &lt;TASK_CREATED_TIME:string`yyyy-mm-ddTHH:mm:ss`&gt;,
    "deadline": &lt;TASK_DEADLINE_TIME:string`yyyy-mm-ddTHH:mm:ss`&gt;,
    "deadlineness": &lt;HAVE_DEADLINE_INDICATOR:boolean&gt;,
    "detail": &lt;TASK_DETAIL:string&gt;,
    "id": &lt;TASK_ID:int&gt;,
    "priority": &lt;TASK_PRIORITY:int&gt;,
    "status": &lt;TASK_STATUS:ref`/status/`&gt;,
    "title": &lt;TASK_TITLE:string&gt;
  }
}
</pre></td>
</tr>

<tr>
<td>
<pre>
POST /api/task
</pre>
</td>
<td>
Create a new task. If sufficient data are provided, a new task will be created in DB.
</td>
<td>
Accept request body parameters, a task in JSON object format:

<pre>
{
  "deadline": &lt;TASK_DEADLINE_TIME:string`yyyy-mm-ddTHH:mm:ss`, required if deadlineness is true&gt;,
  "deadlineness": &lt;HAVE_DEADLINE_INDICATOR:boolean, required &gt;,
  "detail": &lt;TASK_DETAIL:string, required &gt;,
  "priority": &lt;TASK_PRIORITY:int, required &gt;,
  "status": &lt;TASK_STATUS:ref`/status/`, required &gt;,
  "title": &lt;TASK_TITLE:string, required &gt;
}
</pre>
</td>
<td>
The created task will be return, in JSON object format:
<pre>
{
  "status": "ok",
  "tasks": {
    "created_at": &lt;TASK_CREATED_TIME:string`yyyy-mm-ddTHH:mm:ss`&gt;,
    "deadline": &lt;TASK_DEADLINE_TIME:string`yyyy-mm-ddTHH:mm:ss`&gt;,
    "deadlineness": &lt;HAVE_DEADLINE_INDICATOR:boolean&gt;,
    "detail": &lt;TASK_DETAIL:string&gt;,
    "id": &lt;TASK_ID:int&gt;,
    "priority": &lt;TASK_PRIORITY:int&gt;,
    "status": &lt;TASK_STATUS:ref`/status/`&gt;,
    "title": &lt;TASK_TITLE:string&gt;
  }
}
</pre></td>
</tr>

<tr>
<td>
<pre>
POST /api/task/&lt;id&gt;
</pre>
</td>
<td>
Update the data of a specific task. If a correct id and sufficient data are provided, the task with the provided id will be updated in DB.
</td>
<td>
Accept path parameters and request body parameters, a task in JSON object format:

<pre>
id:int - To specify the id of task.
</pre>

<pre>
{
  "deadline": &lt;TASK_DEADLINE_TIME:string`yyyy-mm-ddTHH:mm:ss`, required if deadlineness is true&gt;,
  "deadlineness": &lt;HAVE_DEADLINE_INDICATOR:boolean, required &gt;,
  "detail": &lt;TASK_DETAIL:string, required &gt;,
  "priority": &lt;TASK_PRIORITY:int, required &gt;,
  "status": &lt;TASK_STATUS:ref`/status/`, required &gt;,
  "title": &lt;TASK_TITLE:string, required &gt;
}
</pre>
</td>
<td>
The updated task will be return, in JSON object format:
<pre>
{
  "status": "ok",
  "tasks": {
    "created_at": &lt;TASK_CREATED_TIME:string`yyyy-mm-ddTHH:mm:ss`&gt;,
    "deadline": &lt;TASK_DEADLINE_TIME:string`yyyy-mm-ddTHH:mm:ss`&gt;,
    "deadlineness": &lt;HAVE_DEADLINE_INDICATOR:boolean&gt;,
    "detail": &lt;TASK_DETAIL:string&gt;,
    "id": &lt;TASK_ID:int&gt;,
    "priority": &lt;TASK_PRIORITY:int&gt;,
    "status": &lt;TASK_STATUS:ref`/status/`&gt;,
    "title": &lt;TASK_TITLE:string&gt;
  }
}
</pre></td>
</tr>

<tr>
<td>
<pre>
POST /api/task/&lt;id&gt;
</pre>
</td>
Delete a specific task. If a correct id is provided, the task with the provided id will be delete in DB.
<td>
</td>
<td>
Accept path parameters:

<pre>
id:int - To specify the id of task.
</pre>
</td>
<td>
The id of the deleted task will be return, in JSON object format:
<pre>
{
  "status": "ok",
  "id": &lt;TASK_ID:int&gt;
}
</pre></td>
</tr>
</table>

