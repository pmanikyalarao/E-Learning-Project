        let searchFriend = document.getElementById('searchFriend')
        let searchButton = document.getElementById("searchButton")
        let searchedFriend = document.getElementById("addFriendBlock")

        searchFriend.addEventListener('input',()=>{
            if(searchFriend.value == ""){
                searchButton.style.display = 'none'
            }
            else{
                searchButton.style.display = 'block'
            }
            searchedFriend.style.display = 'none'
        })

        searchFriend.addEventListener('keypress',function(event){
                    if(event.key === 'Enter'){
                        findFriend();
                    }
        })

        function findFriend(){
            searchedFriend.style.display = 'flex'
            req = new XMLHttpRequest()
            req.open('GET','/searchFriend/'+searchFriend.value,true);
            req.onreadystatechange = ()=>{
                if(req.status == 200 && req.readyState == 4){
                    let parent = document.getElementById('searchedFriend')
                    parent.innerHTML = " ";

                    let res = JSON.parse(req.responseText)

                    let div = document.createElement("div");
                    div.classList.add('searchedFicon');

                    let img = document.createElement('img');
                    img.src = "{{ url_for('beforeLoginHome_pg.static',filename='imgs/profileIcon.jpg') }}"

                    let h2 = document.createElement('h2');
                    h2.innerText = searchFriend.value;



                    div.appendChild(img)
                    parent.appendChild(div)
                    parent.appendChild(h2)

                    if(res.check == 'notAdded'){
                        let button = document.createElement('button');
                        button.innerText = 'Add'
                        button.setAttribute('id','addFriend');
                        parent.appendChild(button)
                    }

                }
            }
            req.send()
            searchedFriend.style.display = 'flex'
        }