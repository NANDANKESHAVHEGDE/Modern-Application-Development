const Register = Vue.component('register',{
    template:`
    <div>
    <div>
        <form id="card-update-form">
            <div>
                <h1 style="text-align: center">Register</h1>
                <br>
                <div>
                    <input type="text" name="email" placeholder="email" v-model="email" required />
                </div>
                <div>    
                    <input type="text" name="username" placeholder="username" v-model="username" required />
                </div>
                <div>
                    <input type="text" name="password" placeholder="password" v-model="password" required />
                </div>
            </div>
            <br>
            <div style="text-align: center">
                <input v-on:click="registerUser" type="submit" value="Submit">
            </div>
        </form>
    </div>
    </div>`,
    data: function(){
        return {
            email: null, 
            username: null, 
            password: null, 
        }
    },
    methods:{
        registerUser:async function(evt){
            evt.preventDefault()
            await fetch('http://127.0.0.1:8080/register?include_auth_token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        "email": this.email,
                        "username": this.username,
                        "password": this.password,
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    console.log(data.response.user.authentication_token)
                    localStorage.setItem("username", this.username)
                    localStorage.setItem("token", data.response.user.authentication_token)
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            console.log(this.username)    
            this.$router.push({name:'Dashboard', params:{username:this.username}})
        }
    }
})

const Login = Vue.component('login',{
    template:`
    <div>
    <h1 class="header">Kanban - increase productivity through workflow management</h1>
    <div class="row">
        <form id="login-form">
            <div>
                <h1>Login</h1>
            <br>
                <input type="text" name="uname" placeholder="Username" v-model="username" required />
                <input type="text" name="password" placeholder="Password" v-model="password" required />
            </div>
            <div class="register-spacing">
                <input v-on:click="loginUser" type="submit" value="Submit">
            </div>
            <div class="register-spacing">
                Not registered? 
                <button><router-link to="/register">Click here</router-link></button>  
            </div>
        </form>
    </div>
    <br>
    <table style="width: 100%; border: 4px solid black;" >
        <tr>
            <th>Usage</th>
            <th>Description</th>
        </tr>
        <tr>
            <td>
                <ul>
                    <li>Lists are first added to the board with the name and description</li>
                    <li>Cards can then be added to each list using the respective buttons</li>
                    <li>Use edit option to mark card completion and to move it between lists</li>
                    <li>Deleting a list removes its constituent cards as well</li>
                    <li>Use navigation bar to switch between board view and summary</li>
                </ul>
            </td>
            <td>
                <ol>
                    <li><strong>Board:</strong> The home page containing all the lists and cards. This serves as the main area displaying all the information pertaining to cards</li>
                    <li><strong>List:</strong> A column in the board where cards related to a particular activity can be grouped together</li>
                    <li><strong>Card:</strong> These are individual tasks in a list. The tasks will contain a completion status and can be set to have a deadline associated with the same</li>
                    <li><strong>Summary:</strong> A collective view of the status of cards with records of card completion</li>
                </ol>
            </td>
        </tr>
    </table>
    <h5>The board is best designed to contain upto 5 lists with upto 3 cards in each</h5>
    </div>`,
    data: function(){
        return {
            username: null,
            password: null
        }
    },
    methods:{
        loginUser:async function(evt){
            evt.preventDefault()
            await fetch('http://127.0.0.1:8080/login?include_auth_token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        "username": this.username,
                        "password": this.password
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                    console.log("auth below this")
                    console.log(data.response.user.authentication_token)
                    localStorage.setItem("username", this.username)
                    localStorage.setItem("token", data.response.user.authentication_token)
                    
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
                if (localStorage.getItem("token") != null) 
                    this.$router.push({name:'Dashboard'}) 
                else{alert("Please enter the correct credentials")}    
        }
    }
})

const AddCard = Vue.component('add_card', {	
    props : ["username"],
    template: `
    <div>
    <form method="POST" id="card-update-form">
        <h1>Create a card</h1>
        <div>
            <label>Name: </label>
            <input type="text" name="card_name" v-model="card_name" required/>
        </div>
        <div>
            <label>Content: </label>
            <input type="text" name="card_content" v-model="card_content" required />
        </div>
        <div>
            <label>Deadline: </label>
            <input type="date" name="card_deadline" v-model="card_deadline" required />
        </div>
        <div>
            <label>Completed: </label>
            <select name="card_completion" id="completion" v-model="card_completion">
                <option value="no">No</option>
                <option value="yes">Yes</option>
            </select>
        </div>
        <br>
        <div style="text-align: center;">
            <input v-on:click="createCard($route.params.list_id,$route.params.username)" type="submit" value="Submit">
        </div>
    </form>  
    </div>`,
    data: function() {
        return {
            card_name: null,
            card_content: null,
            card_deadline: null,
            card_completion: null,
        }
    },
    methods: {
        createCard: function(list_id,username){
            r = localStorage.getItem("token")
            fetch('http://127.0.0.1:8080/api/'+username+'/cards/'+list_id, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': r
                    },
                    body: JSON.stringify({
                        "list_id": list_id,
                        "card_name": this.card_name,
                        "card_content": this.card_content,
                        "card_deadline": this.card_deadline,
                        "completion": this.card_completion
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        this.$router.push({name:'Dashboard', params:{username:this.username}})
        }
    }
})

const EditCard = Vue.component('edit_card', {
    props: ["list_id","card_id","card_name","card_content","card_deadline","card_completion","lists","username"],
    template: `
    <div>
    <form method="POST" id="card-update-form">
        <h1>Edit the card</h1>
        <select name="list_id" id="list_id" v-model="list_id">               
            <option v-for="(list,index) in lists" :value="list.list_id">{{list.list_name}}</option>
        </select>
        <div>
            <label>Card name: </label>
            <input type="text" name="card_name" v-model="card_name" required />
        </div>
        <div>
            <label>Content: </label>
            <input type="text" name="card_content" v-model="card_content" required />
        </div>
	    <div>
            <label>Deadline: </label>
            <input type="date" name="card_deadline" v-model="card_deadline" required />
        </div>
        <div>
            <label for="completion">Completed: </label>
            <select name="card_completion" id="completion" v-model="card_completion">                
                <option value="no">No</option>
                <option value="yes">Yes</option>
            </select>
        </div>
        <div style="text-align: center;">
            <input v-on:click="EditCard(list_id,card_id,username)" type="submit" value="Submit">
        </div>
    </form>
    </div>`,
    data: function() {
        return {
        }
    },
    methods: {
        EditCard: function(list_id,username,card_id){
            r = localStorage.getItem("token")
            fetch('http://127.0.0.1:8080/api/'+ this.username+'/cards/'+list_id+"/"+ this.card_id, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': r
                    },
                    body: JSON.stringify({
                        "list_id": this.list_id,
                        "card_name": this.card_name,
                        "card_content": this.card_content,
                        "card_deadline": this.card_deadline,
                        "completion": this.card_completion
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        this.$router.push({name:'Dashboard', params:{username:this.username}})    
        }
    }
})

const EditList = Vue.component('edit_list', {
    props:["list_id", "list_name", "list_description", "username"],		
    template: `
    <div>
    <form method="POST" id="list-update-form">
        <h1 style="text-align: center;">Edit the list</h1>
        <div>
            <label>List name:</label>
            <input type="text" name="list_name" v-model="list_name" required/>
        </div>
        <div>
            <label>List desc:</label>
            <input type="text" name="list_desc" v-model="list_description" required/>
        </div>
        <br>
        <div style="text-align: center;">
            <input v-on:click="EditList(list_id)" type="submit" value="Submit">
        </div>
    </form>
    </div>`,
    data: function() {
        return {
        }
    },
    methods: {
        EditList: function(list_id){
            r = localStorage.getItem("token")
            fetch('http://127.0.0.1:8080/api/'+this.username+'/'+list_id, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': r
                    },
                    body: JSON.stringify({
                        "list_name": this.list_name,
                        "list_desc": this.list_description
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        this.$router.push({name:'Dashboard', params:{username:this.username}})     
        }
    }
})

const AddList = Vue.component('add_list', {
    props: ["username"],
    template: `
    <div>
    <form action="/" method="POST" id="list-update-form">
        <h1>Create a list</h1>
        <div>
            <label>Name: </label>
            <input type="text" name="list_name" v-model="list_name" required/>
        </div>
        <div>
            <label>Description: </label>
            <input type="text" name="list_description" v-model="list_description" required/>
        </div>    
        <br>
        <div style="text-align: center;">
            <input v-on:click="createList" type="submit" value="Submit">
        </div>
    </form>
    </div>`,
    data: function() {
        return {
            list_name: null,
            list_description: null,
        }
    },
    methods: {
        createList: function(evt){
            evt.preventDefault()
            r = localStorage.getItem("token")
            console.log(r)
            console.log(this.username)
            fetch('http://127.0.0.1:8080/api/'+this.username, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': r
                    },
                    body: JSON.stringify({
                        "list_name": this.list_name,
                        "list_desc": this.list_description
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        this.$router.push({name:'Dashboard', params:{username:this.username}})  
        }
    },
    mounted: function(){
        console.log(this.username)
    }
})

const SummaryPage = Vue.component('summarypage', {
    template:`
    <div>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand" href="#">Welcome: {{username}}</a>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item">
                        <a class="navbar-brand"></a>
                    </li>
                </ul>  
                <ul class="navbar-nav">
                    <li class="nav-item"><router-link class="nav-link" :to="{name: 'Dashboard', params: {username: username}}">Home</router-link> </li>
                    <li class="nav-item" v-on:click="csvExport(username)"><router-link class="nav-link" :to="{name: 'Dashboard', params: {username: username}}">Export</router-link> </li>
                    <li class="nav-item"><router-link class="nav-link" to="/summarypage">Summary</router-link> </li>
                    <li class="nav-item" v-on:click="userLogout()"><router-link  class="nav-link" to="/">Logout</router-link></li>
                </ul>
            </div>
        </nav>
        <div>
            <img alt="Trendline of cards completed" id="timeline"/>
            <img alt="Completion share of cards" id="compstat"/>
        </div>
        <table style="width: 80%; border: 5px solid black">
            <tr>
                <th style="width: 5%">List ID</th>
                <th style="width: 25%">List name</th>
                <th style="width: 5%">Completed cards</th>
                <th style="width: 5%">Incomplete cards</th>
                <th style="width: 5%">Deadline crossed</th>
            </tr>
            <tr v-for="(list,index) in lists">
                <td>{{list[0]}}</td>
                <td>{{list[1]}}</td>
                <td>{{list[2]}}</td>
                <td>{{list[3]}}</td>
                <td>{{list[4]}}</td>
            </tr>
        </table>
    </div>
    `,
    data: function() {
        return {
            message1: "Test name",
            message2: "",
            lists: [],
            username: localStorage.getItem("username")
        }
    },
    methods: {
        userLogout: function(){
            fetch("http://127.0.0.1:8080/logout")
            localStorage.removeItem("token")
            localStorage.removeItem("username")
            console.log("Logging out user")
        },
        csvExport: function(username){
            t = localStorage.getItem("token")
            alert("The file has been sent to your registered email address")
            fetch("http://127.0.0.1:8080/api/"+username+"/export",{
                headers: {
                    Accept: '*/*',
                    'Authentication-Token': t
                }
            })
            console.log("Exported")
        }
    },
    mounted: async function() {
        t = localStorage.getItem("token")
        await fetch("/api/"+this.username+"/timeline", {
            headers: {
                Accept: '*/*',
                'Authentication-Token': t
            }
        }).then(res => res.blob())
        .then(data => {
            let url = URL.createObjectURL(data)
            let elem = document.getElementById("timeline")
            elem.src = url
        })        
        fetch("/api/"+this.username+"/compstat", {
            headers: {
                Accept: '*/*',
                'Authentication-Token': t
            }
        }).then(res => res.blob())
        .then(data => {
            let url = URL.createObjectURL(data)
            let elem = document.getElementById("compstat")
            elem.src = url
        })
        l = await fetch("http://127.0.0.1:8080/api/"+this.username+"/sumtable", {
            headers: {
                Accept: '*/*',
                'Authentication-Token': t
            }
        })
        m = await l.json()
        this.lists = m
    }
})


const Dashboard = Vue.component('dashboard', {
    template: `
    <div>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand" href="#">Welcome: {{username}}</a>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item">
                        <a class="navbar-brand"></a>
                    </li>
                </ul>  
                <ul class="navbar-nav">
                    <li class="nav-item"><router-link class="nav-link" to="/dashboard">Home</router-link> </li>
                    <li class="nav-item" v-on:click="csvExport(username)"><router-link class="nav-link" to="/dashboard">Export</router-link> </li>
                    <li class="nav-item"><router-link class="nav-link" :to="{name: 'SummaryPage', params: {username: username}}">Summary</router-link> </li>
                    <li class="nav-item" v-on:click="userLogout()"><router-link  class="nav-link" to="/">Logout</router-link></li>
                </ul>
            </div>
        </nav>
        <div class="col_list" v-for="(list,index) in lists"> 
            <div class="lists">
                {{list.list_name}}<button v-on:click="removeList(list.list_id, index)">Del</button>
                <button>
                    <router-link :to="{name: 'EditList', params: {list_id: list.list_id, list_name: list.list_name, list_description: list.list_desc, username: username}}">Edit</router-link>
                </button>
                <button v-on:click="exportList(username,list.list_id)">Exp</button>
            </div>     
            <div v-for="(card,index) in cards">
                <div class="card_ui" v-if="list.list_id == card.list_id">
                    <div><strong>Name:</strong> {{card.card_name}}</div>
            		<div><strong>Content:</strong> {{card.card_content}}</div>
            		<div><strong>Deadline:</strong> {{card.card_deadline}}</div>
            		<div style="color: red" v-if="card.completion == 'no'"><strong style="color: black">Status:</strong> Incomplete</div>
            		<div v-if="card.completion == 'yes'"><strong>Status:</strong> Complete</div>
                    <div style="width: 50%; margin: 0 auto">
                    <button v-on:click="removeCard(card.list_id,card.card_id, index)">Del</button>
                    <button><router-link :to="{name: 'EditCard', params: {list_id: card.list_id, card_id: card.card_id, card_name: card.card_name, card_content: card.card_content,card_deadline: card.card_deadline, card_completion: card.completion, lists: lists,username: username}}">Edit</router-link></button></div>
                </div>
            </div>
            <p class="add_card">
            <button>
                <router-link :to="{name: 'AddCard', params: {list_id: list.list_id, username: username}}" >Add Card</router-link>
            </button>
            </p>
        </div>
    <button>
        <router-link :to="{name: 'AddList', params: {username: username}}">Add List</router-link>
    </button>
    </div>
        `,
    data: function() {
        return {
            cards: [],
            lists: [],
            username: localStorage.getItem("username"),
        }
    },
    methods: {
        removeList: function(list_id, index){
            t = localStorage.getItem("token")
            fetch("http://127.0.0.1:8080/api/"+ this.username +"/"+list_id, {
                method: 'DELETE',
                headers: {
                    Accept: '*/*',
                    'Authentication-Token': t
                },
            })
            .then(() => {
                this.lists.splice(index, 1)
            })
        },
        removeCard: function(list_id,card_id,index){
            t = localStorage.getItem("token")
            fetch("http://127.0.0.1:8080/api/"+this.username+"/cards/"+list_id+"/"+card_id, {
                method: 'DELETE',
                headers: {
                    Accept: '*/*',
                    'Authentication-Token': t
                },
            })
            .then(() => {
                this.cards.splice(index, 1)
            })
        },
        csvExport: function(username){
            t = localStorage.getItem("token")
            alert("The file has been sent to your registered email address")
            fetch("http://127.0.0.1:8080/api/"+username+"/export",{
                headers: {
                    Accept: '*/*',
                    'Authentication-Token': t
                }
            })
            console.log("Exported")
        },
        exportList: function(username, list_id){
            t = localStorage.getItem("token")
            alert("The file has been sent to your registered email address")
            fetch("http://127.0.0.1:8080/api/"+username+"/"+list_id+"/export",{
                headers: {
                    Accept: '*/*',
                    'Authentication-Token': t
                }
            })
        },
        userLogout: function(){
            fetch("http://127.0.0.1:8080/logout")
            localStorage.removeItem("token")
            localStorage.removeItem("username")
            console.log("Logging out user")
        }
    },

    mounted: async function() {
        t = localStorage.getItem("token")
    	r = await fetch("http://127.0.0.1:8080/api/"+this.username+"/cards", {
            headers: {
                Accept: '*/*',
                'Authentication-Token': t
            }
        })
        d = await r.json()
        this.cards = d
        l = await fetch("http://127.0.0.1:8080/api/"+this.username, {
            headers: {
                Accept: '*/*',
                'Authentication-Token': t
            }
        })
        m = await l.json()
        this.lists = m
    }
})

const NotFound = { template: '<p>Page not found</p>' }

const routes = [{
    path: '/',
    component: Login
}, {
    path: '/register',
    name: 'Register',
    component: Register
}, {
    path: '/summarypage',
    name: 'SummaryPage',
    component: SummaryPage,
    props: true
}, {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    props: true
}, {
    path: '/edit_list',
    name: 'EditList',
    component: EditList,
    props: true
}, {
    path: '/edit_card',
    name: 'EditCard',
    component: EditCard,
    props: true
}, {
    path: '/add_list',
    name: 'AddList',
    component: AddList,
    props: true
}, {
    path: '/add_card',
    name: 'AddCard',
    component: AddCard,
    props: true
}
];

const router = new VueRouter({
  routes 
})


var app = new Vue({
    el: '#app',
    router: router,
    data: {
        user_name: "Randomtext"
    },
    methods: {
        test_method: function() {
            console.log("I am within test method function")
        }
    }

})
