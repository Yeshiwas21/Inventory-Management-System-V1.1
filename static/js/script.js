
document.addEventListener("DOMContentLoaded", function () {
  var parentListItems = document.querySelectorAll('.parent-list > li');

  parentListItems.forEach(function (item) {
      item.addEventListener('click', function () {
          var nestedList = this.querySelector('.nested-list');
          
          // Hide all other nested-lists
          parentListItems.forEach(function (otherItem) {
              if (otherItem !== item) {
                  var otherNestedList = otherItem.querySelector('.nested-list');
                  if (otherNestedList) {
                      otherNestedList.style.display = 'none';
                  }
              }
          });

          // Toggle the display of the clicked nested-list
          if (nestedList) {
              nestedList.style.display = (nestedList.style.display === 'none' || nestedList.style.display === '') ? 'block' : 'none';
          }
      });
  });
});
