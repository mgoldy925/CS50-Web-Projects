document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email('', '' ,''));

  // By default, load the inbox
  load_mailbox('inbox');

  // Add event listener for compose email
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // Add event listener to archive button
  document.querySelector('#archive').addEventListener('click', function() {

    // Get id from form
    var btn = document.querySelector('#archive');
    var id = btn.value;
    var archived = (btn.innerHTML == 'Archive'); // Assuming will be 'Archive' or 'Unarchive'

    // Set to archived/unarchived
    fetch(`/emails/${id}`, {
      method: "PUT",
      body: JSON.stringify({
        archived: archived
      })
    })
    .then(() => {
      // Redirect to inbox
      load_mailbox('inbox');
    });
  });

  // Add event listener to reply button
  document.querySelector('#reply').addEventListener('click', function() {
    
    // Get id and fetch info about email
    var id = document.querySelector('#reply').value;
    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      // Format info
      r = email.sender;
      s = `Re: ${email.subject}`;
      b = `\n\n\nOn ${email.timestamp}, ${email.sender} wrote:\n${email.body}`;
      compose_email(r, s, b);
    });
  });

});

function compose_email(r ,s, b) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = r;
  document.querySelector('#compose-subject').value = s;
  document.querySelector('#compose-body').value = b;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Delete emails currently there
  document.querySelector('#emails-view').innerHTML = '';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails in mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Display emails
    emails.forEach(function(email) {
      const email_div = create_email(document.createElement('div'), email);
      // Add event listener for clicking on an email
      email_div.addEventListener('click', function() { display_email(email.id); });
      document.querySelector('#emails-view').append(email_div);
    });
  });
}

function email_view(email) {
  
  // Show email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // Display email
  document.querySelector('#subject').innerHTML = email.subject;
  document.querySelector('#sender').innerHTML = "<b>From:</b>  " + email.sender;
  document.querySelector('#timestamp').innerHTML = email.timestamp;
  document.querySelector('#recipients').innerHTML = "<b>To:</b>  " + email.recipients;
  document.querySelector('#body').innerHTML = email.body;

  // Add to reply button to get id for reply, could just reuse archive button but wanna keep them separate
  document.querySelector('#reply').value = email.id;

  // Handle archive/unarchive button
  var btn = document.querySelector('#archive');
  btn.innerHTML = email.archived ? 'Unarchive' : 'Archive';  
  btn.value = email.id;
}

function create_email(email_div, email) {

  // elements = <p>'s, info = info to put into <p>'s
  var elements = new Array(3);
  var info = new Array(email.sender, email.subject, email.timestamp);

  for (var i = 0; i < 3; i++) {
    // Create element, add info, give it class to style, and add it to div
    elements[i] = document.createElement('p');
    elements[i].innerHTML = info[i];
    elements[i].classList.add(`email-div-${i+1}`);
    email_div.append(elements[i]);
  }

  // Add class to style, check if it's read in order to change background color
  email_div.classList.add('email-div');
  if (email.read) {
    email_div.style.backgroundColor = 'lightgray';
  }
  return email_div;
}

function send_email() {

  // Get info to post to API
  recipients = document.querySelector('#compose-recipients').value;
  subject = document.querySelector('#compose-subject').value;
  body = document.querySelector('#compose-body').value;

  // Make post request
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
  });

  // Redirect to inbox and return false as to not refresh page
  load_mailbox('inbox');
  return false;
}

function display_email(id) {
  
  // Get email
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    // Set email as read and display it
    email_view(email);
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    });
  });
}

function reply(email) {

}