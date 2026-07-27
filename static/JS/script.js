document.querySelectorAll(".task-link").forEach(function(task){

    task.addEventListener("click", function(e){ 
        e.preventDefault();
        let id = this.dataset.id;

        fetch(`/completed/${id}`, {
            method:"POST"
        })

        .then(response => response.json())
        .then(data => {
            let li = this.closest("li");
            if(data.completed){
                li.classList.add("completed");
            }
            else{
                li.classList.remove("completed");
            }
        });
    });
});