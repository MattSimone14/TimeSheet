% rebase('layout.tpl', title='edit hours')

<form action="/editHours" method="post">
	<h2>Enter emp_id and Hours Worked</h2>

	<p><input type='text' name='eid' size='5'> employee ID</p>
	<p><input type='text' name='hrs' size='5'> Enter hrs worked</p>

	<p><input type="submit" value='Submit Query'></p>
    <br>
</form>