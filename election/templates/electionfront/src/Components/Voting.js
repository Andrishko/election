import React, {useEffect, useState} from 'react';
import axios from "axios";
import {useNavigate} from "react-router-dom";


const Voting = (props) => {
    let [elect, setElect] = useState()
    let [candidates, setCandidates] = useState([])
    let [faculty, setFaculty] = useState()
    const navigate = useNavigate();


    let getCandidates = async (faculty) => {
        console.log(faculty)
        let response = await axios.post('http://127.0.0.1:8000/api/getcandidates', {
            faculty: faculty
        })
        console.log(response)
        let candidates = response.data
        setCandidates(candidates)
    }

    let getFaculty = async () => {
        console.log('get candidates')
        await axios.post('http://127.0.0.1:8000/api/getfaculty', {
            token: props.token
        }).then(r => {
            setFaculty(r.data)
            console.log(r.data)
            getCandidates(r.data)
        })
    }

    useEffect(() => {
        getFaculty()
    }, [])

    let onChangeValue = (event) => {
        console.log('work')
        console.log(event.target.value)
        setElect(event.target.value)
    }

    let vote = () => {

        if (props.isVoted) {
            window.location.reload()
        } else {
            axios.put('http://127.0.0.1:8000/api/vote', {
                candidate: elect,
                faculty: faculty
            }).then(r => {
                console.log(r.data)
                props.isVoted = true
                if (props.isVoted == true && r.data=='true') navigate('/thanks')
                else navigate('/voting-expired')

            })

        }

    }

    let candidatesElements = candidates.map((candidate) => {
        console.log(candidate)
        return (<div onChange={onChangeValue}>
            <input type="radio" value={candidate.candidate_name} name='candidate'/>{candidate.candidate_name}
        </div>)
    })


    return (
        <div>
            {candidatesElements}
            <button onClick={vote}>VOTE</button>
        </div>
    );
};

export default Voting;