
    mybutton = document.getElementById("myBtn");


    window.onscroll = function() {scrollFunction()};

    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            mybutton.style.display = "block";
        } else {
            mybutton.style.display = "none";
        }
    }

    function topFunction() {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    }


    document.getElementById('date').addEventListener('change', function () {
        updateAvailableTimeSlots();
    });

    updateAvailableTimeSlots();

    function updateAvailableTimeSlots() {
        var selectedDate = new Date(document.getElementById('date').value);
        var dayOfWeek = selectedDate.getDay();

        var timeSelect = document.getElementById('time');
        timeSelect.innerHTML = ''; 

        if (dayOfWeek >= 1 && dayOfWeek <= 5) { 
            addTimeOption('09:00');
            addTimeOption('10:00');
            addTimeOption('11:00');
            addTimeOption('12:00');
            addTimeOption('15:00');
            addTimeOption('16:00');
            addTimeOption('17:00');
        } else if (dayOfWeek === 6) { 
            addTimeOption('09:00');
            addTimeOption('10:00');
            addTimeOption('11:00');
            addTimeOption('12:00');
        } else {
            // Handle other days (Sunday) if needed
        }
    }

    function addTimeOption(time) {
        var option = document.createElement('option');
        option.value = time;
        option.text = time;
        document.getElementById('time').add(option);
    }