import JSConfetti from 'js-confetti'
export default function Button(){
    const jsConfetti= new JSConfetti()
    const confetti=()=>{
        
        jsConfetti.addConfetti(
        {
         emojis:['🥩','🍞'],
         emojiSize: 150,
         confettiNumber: 30,
        })


    }
    return (

        <button onClick={confetti} className='confettiButton'>PRESS TO CELEBRATE</button>

    );




}