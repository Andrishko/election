import './App.css';
import {Routes, Route,} from 'react-router-dom';
import Voting from "./Components/Voting";
import Thanks from "./Components/Thanks";
import VotingExpired from "./Components/VotingExpired";


function App(props) {
    let url = window.location.href
    console.log(url)
    let url_arr = url.split('/')
    console.log((url_arr))
    let token = url_arr[url_arr.length - 2]

    console.log(token)
    return (

        <div className="App">
            <Routes>
                <Route path={`/api/check/${token}`} element={<Voting isVoted={props.isVoted} token={token}/>}/>
                <Route path={`/thanks`} element={<Thanks/>}/>
                <Route path={`/voting-expired`} element={<VotingExpired/>}/>
            </Routes>
        </div>
    );
}

export default App;
