const scholarshipContainer = document.querySelector('.scholarships-container');

fetch('/scholarships')  // Fetch scholarship data
  .then(response => response.json())
  .then(data => {
    data.forEach(scholarship => {
      const card = document.createElement('div');
      card.classList.add('scholarship-card');

      const title = document.createElement('h3');
      title.classList.add('scholarship-title');
      title.textContent = scholarship.title;

      const description = document.createElement('p');
      description.classList.add('scholarship-description');
      description.textContent = scholarship.description;

      const eligibility_criteria = document.createElement('p');
      deadline.classList.add('scholarship-eligibility_criteria');
      deadline.textContent = `eligibility_criteria: ${scholarship.eligibility_criteria}`;

      const deadline = document.createElement('p');
      deadline.classList.add('scholarship-deadline');
      deadline.textContent = `Deadline: ${scholarship.deadline}`;

      const contact_details = document.createElement('p');
      deadline.classList.add('scholarship-contact_details');
      deadline.textContent = `contact_details: ${scholarship.contact_details}`;

      const link_to_more_information = document.createElement('p');
      deadline.classList.add('scholarship-link_to_more_information');
      deadline.textContent = `link_to_more_information: ${scholarship.link_to_more_information}`;

      card.appendChild(title);
      card.appendChild(description);
      card.appendChild(deadline);
      card.appendChild(eligibility_criteria);
      card.appendChild(contact_details);
      card.appendChild(link_to_more_information);

      scholarshipContainer.appendChild(card);
    });
  })
  .catch(error => console.error(error));
  

const readMoreBtns = document.querySelectorAll('.read-more-btn');

readMoreBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const details = btn.nextElementSibling;
    details.style.display = details.style.display === 'none' ? 'block' : 'none';
    const editDeleteBtns = details.querySelector('.edit-delete-buttons');
    editDeleteBtns.style.display = editDeleteBtns.style.display === 'none' ? 'block' : 'none';
  });
});

const saveBtns = document.querySelectorAll('.save-btn');

saveBtns.forEach(btn => {
  btn.addEventListener('click', async () => {
    const scholarshipId = btn.dataset.scholarshipId;

    try {
      const response = await fetch(`/scholarships/${scholarshipId}/save`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to save scholarship');
      }

      const data = await response.json();
      alert(data.message);

    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while saving scholarship');
    }
  });
});

const deleteBtns = document.querySelectorAll('.delete-btn');

deleteBtns.forEach(btn => {
  btn.addEventListener('click', (event) => {
    event.preventDefault();

    const confirmation = confirm('Are you sure you want to delete this scholarship?');
    if (confirmation) {
      btn.parentElement.submit();
    }
  });
});
