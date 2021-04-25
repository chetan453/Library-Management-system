# system
<h1> Library management system </h1>
<h3>This website has 3 user </h3>
<ul>
  <li> librarian-which has access to the books can change details ,add books and can approve or reject borrow request raised by student</li>
  <li> Student - which has access to the book can raise the borrow request for the book </li>
  <li> Admin - which has access to everything can add/remove student,librarian can approve the sign request for the librarian
</ul>


<p> our library management system has very basic feature student can see raise borrow request can see their profile and has access to the book.librarian can see the profile of the student
and borrowing request of the user.</p>

site has some bug which are the librarian can also raise the borrow request which i didn't want that happens.I tried to remove this bug by restricting borrow form only to group student
but when I used if statement in html files to access the group of the user it throws an error. because the details page of book is same for student and librarian.
