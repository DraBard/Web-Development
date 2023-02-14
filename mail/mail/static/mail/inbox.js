document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // 1:08:30 CS50W Javascript lectures
  document.querySelector('form').onsubmit = () => send_email();

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email_id-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email_id-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  if (mailbox === "inbox") {
    fetch('/emails/inbox')
    .then(response => response.json())
    .then(emails => {

    for (var i = 0; i < emails.length; i++) {
      let email = emails[i];
      var item = document.createElement("div");
      item.style.display = "flex";
      item.style.justifyContent = "space-between";
      item.style.border = "1px solid black";
      item.style.padding = "10px";
      if (email.read === true) {
        item.style.backgroundColor = "gray"
      }

      var sender = document.createElement("span");
      sender.innerHTML = email.sender;
      sender.style.width = "10%";

      var subject = document.createElement("span");
      subject.innerHTML = email.subject;
      subject.style.width = "60%";

      var timestamp = document.createElement("span");
      timestamp.innerHTML = email.timestamp;

      item.appendChild(sender);
      item.appendChild(subject);
      item.appendChild(timestamp);
      // Add the function as well
      item.addEventListener('click', () => load_email(email.id, true));

      document.querySelector('#emails-view').appendChild(item);
  }})}

  if (mailbox === "sent") {
    fetch('/emails/sent')
    .then(response => response.json())
    .then(emails => {

    for (var i = 0; i < emails.length; i++) {
      var email = emails[i];
      var item = document.createElement("div");
      item.style.display = "flex";
      item.style.justifyContent = "space-between";
      item.style.border = "1px solid black";
      item.style.padding = "10px";

      var recipients = document.createElement("span");
      recipients.innerHTML = email.recipients;
      recipients.style.width = "10%";

      var subject = document.createElement("span");
      subject.innerHTML = email.subject;
      subject.style.width = "60%";

      var timestamp = document.createElement("span");
      timestamp.innerHTML = email.timestamp;

      item.appendChild(recipients);
      item.appendChild(subject);
      item.appendChild(timestamp);

      document.querySelector('#emails-view').appendChild(item);
  }})}

  if (mailbox === "archive") {
    fetch('/emails/archive')
    .then(response => response.json())
    .then(emails => {

    for (var i = 0; i < emails.length; i++) {
      var email = emails[i];
      var item = document.createElement("div");
      item.style.display = "flex";
      item.style.justifyContent = "space-between";
      item.style.border = "1px solid black";
      item.style.padding = "10px";

      var recipients = document.createElement("span");
      recipients.innerHTML = email.recipients;
      recipients.style.width = "10%";

      var subject = document.createElement("span");
      subject.innerHTML = email.subject;
      subject.style.width = "60%";

      var timestamp = document.createElement("span");
      timestamp.innerHTML = email.timestamp;

      item.appendChild(recipients);
      item.appendChild(subject);
      item.appendChild(timestamp);
      item.addEventListener('click', () => load_email(email.id, false));

      document.querySelector('#emails-view').appendChild(item);
  }})}

}

function send_email() {

  // event.preventDefault()

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

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
      // Print result
      console.log(result);
  });
  load_mailbox("sent");
}


function load_email(email_id, to_archive) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email_id-view').style.display = 'block';

  document.querySelector('#email_id-view').innerHTML = "";

  fetch('/emails/' + email_id)
  .then(response => response.json())
  .then(email => {
  // Print email
  // console.log(email);

  var sender = document.createElement("div");
  sender.innerHTML = "<strong>From: </strong>" + email.sender;
  document.querySelector('#email_id-view').appendChild(sender);

  var recipients = document.createElement("div");
  recipients.innerHTML = "<strong>To: </strong>" + email.recipients;
  document.querySelector('#email_id-view').appendChild(recipients);

  var subject = document.createElement("div");
  subject.innerHTML = "<strong>Subject: </strong>" + email.subject;
  document.querySelector('#email_id-view').appendChild(subject);

  var timestamp = document.createElement("div");
  timestamp.innerHTML = "<strong>Timestamp: </strong>" + email.timestamp;
  document.querySelector('#email_id-view').appendChild(timestamp);

  var reply_button = document.createElement("button");
  reply_button.innerHTML = "Reply";
  reply_button.classList.add("btn");
  reply_button.classList.add("btn-sm");
  reply_button.classList.add("btn-outline-primary");
  reply_button.style.marginRight = "10px";
  reply_button.id = "reply-button";
  reply_button.addEventListener('click', () => reply(email.recipients, email.subject, email.timestamp, email.body));
  document.querySelector('#email_id-view').appendChild(reply_button);

  let archive_button = document.createElement("button");
  archive_button.classList.add("btn");
  archive_button.classList.add("btn-sm");
  archive_button.classList.add("btn-outline-primary");
  archive_button.id = "archive-button";
  if (to_archive === true) {
    archive_button.innerHTML = "Archive";
    archive_button.addEventListener('click', () => move_to_archive(email.id, true));
  }
  else {
    archive_button.innerHTML = "Unarchive";
    archive_button.addEventListener('click', () => move_to_archive(email.id, false));
  }
  document.querySelector('#email_id-view').appendChild(archive_button);


  var body = document.createElement("div");
  body.innerHTML = email.body;
  document.querySelector('#email_id-view').appendChild(body);

  fetch('/emails/' + email_id, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
  })})
  })
}


function move_to_archive(email_id, to_archive) {

  fetch('/emails/' + email_id, {
    method: 'PUT',
    body: JSON.stringify({
        archived: to_archive
  })})
}


function reply(recipients, subject, timestamp, body) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email_id-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;

  try {
    let re_part = /^Re:/.exec(subject)[0];
      document.querySelector('#compose-subject').value = subject;
  } catch (error) {
    // Handle the case where the regular expression does not match the subject string
    document.querySelector('#compose-subject').value = "Re: " + subject;
  }

  document.querySelector('#compose-body').value = "On " + timestamp + " " + recipients + " wrote: " + body;

}