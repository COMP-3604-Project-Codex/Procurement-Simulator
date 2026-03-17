// Add/Edit Lot Modal Logic

document.addEventListener('DOMContentLoaded', function () {
  const addLotBtn = document.getElementById('add-lot-btn');
  const addLotModal = document.getElementById('add-lot-modal');
  const editLotModal = document.getElementById('edit-lot-modal');
  const closeModalBtns = document.querySelectorAll('.close-modal');
  const editLotBtns = document.querySelectorAll('.edit-lot-btn');
  const editLotForm = document.getElementById('edit-lot-form');

  // Show Add Lot Modal
  if (addLotBtn && addLotModal) {
    addLotBtn.addEventListener('click', function () {
      addLotModal.classList.remove('hidden');
    });
  }

  // Show Edit Lot Modal
  editLotBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      const lotId = btn.getAttribute('data-lot-id');
      // Fetch lot data from DOM
      const lotCard = btn.closest('.rounded-2xl');
      const labType = lotCard.querySelector('div:nth-child(2) > div:nth-child(1)').textContent.replace('Lab Type : ', '').trim();
      const labSize = lotCard.querySelector('div:nth-child(2) > div:nth-child(2)').textContent.replace('Lab Size : ', '').trim();
      const budget = lotCard.querySelector('div:nth-child(2) > div:nth-child(3)').textContent.replace('Budget : $', '').replace(/,/g, '').trim();
      document.getElementById('edit-lab-type').value = labType;
      document.getElementById('edit-lab-size').value = labSize;
      document.getElementById('edit-budget').value = budget;
      editLotForm.action = `/admin/lots/${lotId}/edit`;
      editLotModal.classList.remove('hidden');
    });
  });

  // Close Modals
  closeModalBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      addLotModal.classList.add('hidden');
      editLotModal.classList.add('hidden');
    });
  });

  // Hide modals on outside click
  [addLotModal, editLotModal].forEach(function (modal) {
    if (modal) {
      modal.addEventListener('click', function (e) {
        if (e.target === modal) {
          modal.classList.add('hidden');
        }
      });
    }
  });
});
