document.addEventListener('DOMContentLoaded', () =\> {

// personal/social codes: 0.5=+?, 0=\~?, -0.5=-?, 1==, -1=\<, 2=\>

const metaStates = {

exploration: "\<strong\>Exploration:\</strong\> Acting without personal or social knowledge. The primary dynamic is navigating mutual uncertainty and inquiry.",

social_navigation: "\<strong\>Social Navigation:\</strong\> Acting without personal knowledge in a world of social judgment. The primary dynamic is reacting to or conforming to a pre-existing social reality.",

influence: "\<strong\>Influence:\</strong\> Acting with personal knowledge in a world of social uncertainty. The primary dynamic is the attempt to teach, persuade, or warn an undecided collective.",

conviction: "\<strong\>Conviction:\</strong\> Acting with personal knowledge in a world of social judgment. The primary dynamic is the alignment or conflict of established beliefs."

};

const hegemonyContexts = {

goodTruth: {

101: { v: 0.9, p: 0.9, j: "Correctly identifying and pursuing a good truth is a highly constructive, high-will action." },

102: { v: 0.8, p: 0.7, j: "Independently pursuing a good truth is highly constructive and requires significant will." },

103: { v: 0.9, p: 1.0, j: "Pursuing a good truth against active suppression is a supreme act of constructive will." },

104: { v: 0.8, p: 0.6, j: "Seeking to understand and join a good consensus is highly constructive." },

105: { v: 0.2, p: 0.7, j: "Questioning a consensus that is actually a good truth is morally neutral but shows high will." },

106: { v: 0.9, p: 0.9, j: "Bravely seeking to understand a good truth despite social outrage is peak constructive behavior." },

201: { v: 0.2, p: -0.4, j: "Passively accepting a good truth is minimally constructive and requires no will." },

202: { v: 0.0, p: -1.0, j: "Mutual apathy towards a good truth is a null state of no will and no moral impact." },

203: { v: -0.1, p: -0.6, j: "Ignoring a good truth because others are is a low-will act of minor destructive consequence." },

204: { v: 0.4, p: -0.2, j: "Conforming to a good truth without understanding is passively constructive but low-will." },

205: { v: -0.5, p: -0.5, j: "Defaulting to a lie when the consensus is a good truth is a destructive, low-will act of delusion." },

206: { v: -0.4, p: -0.3, j: "Avoiding a good truth due to social conflict is a low-will, destructive choice." },

301: { v: -0.8, p: 0.7, j: "Actively resisting the pursuit of a good truth is a high-will, highly destructive act." },

302: { v: -0.7, p: -0.5, j: "Willfully ignoring a good truth, even in apathy, is a destructive act of low will." },

303: { v: -0.9, p: 0.8, j: "A mutual pact to ignore a good truth is a high-will, highly destructive collaboration." },

304: { v: -1.0, p: 0.9, j: "Actively denying a good, consensus truth is the peak of high-will destructiveness (the Greater Lie)." },

305: { v: -0.8, p: -0.2, j: "Willful ignorance validated by a (misperceived) consensus lie is highly destructive." },

306: { v: -0.9, p: 0.2, j: "Refusing to learn a good truth out of fear is a willful act of destruction." },

401: { v: 1.0, p: 0.9, j: "Teaching a good truth to a willing audience is the peak of constructive, high-will action." },

402: { v: 0.2, p: -0.3, j: "Hoarding a good truth is a low-will act that provides minimal constructive value." },

403: { v: 0.6, p: 0.6, j: "Trying to teach a good truth to the willfully ignorant is a constructive, high-will struggle." },

2: { v: 0.9, p: 0.4, j: "Correctly aligning with a good truth is highly constructive." },

1: { v: -0.7, p: 0.9, j: "Believing a good truth is a lie is a high-will, destructive delusion." },

3: { v: -0.8, p: 1.0, j: "Perceiving a good truth as an insult is a supreme act of destructive will." },

501: { v: -0.8, p: 0.7, j: "Incorrectly 'debunking' a good truth is a high-will, destructive act." },

502: { v: -0.7, p: -0.4, j: "Knowing a good truth is false and not caring is a destructive state of apathy." },

503: { v: -0.8, p: -0.5, j: "Giving up trying to disprove a good truth is a destructive, low-will state." },

5: { v: -0.9, p: 0.8, j: "The Cassandra: Correctly identifying the social delusion about a good truth, but being powerless." },

4: { v: 0.9, p: 0.3, j: "Correctly identifying a good truth, even if misperceiving the social view, is highly constructive." },

6: { v: -0.8, p: 0.5, j: "Perceiving a good truth as both a lie and an insult is a destructive delusion." },

601: { v: -0.9, p: 0.8, j: "Preaching outrage against a good truth is a high-will, highly destructive act." },

602: { v: -0.8, p: -0.2, j: "Being insulted by a good truth, even in isolation, is a destructive state." },

603: { v: -0.9, p: 0.9, j: "Trying to force others to reject a good truth is a high-will, highly destructive act." },

8: { v: -1.0, p: 0.9, j: "Conspiring against a good truth is peak destructiveness." },

7: { v: 0.7, p: 0.8, j: "Being insulted by a (misperceived) lie when the reality is a good truth is a high-will, constructive act of a mistaken guardian." },

9: { v: 1.0, p: 1.0, j: "Being insulted by a (misperceived) insult when the reality is a good truth is the ultimate act of a mistaken, but high-will, protector." },

},

badTruth: {

101: { v: -0.5, p: 0.8, j: "Collaboratively pursuing a harmful truth, while intellectually honest, has a negative moral outcome." },

102: { v: -0.4, p: 0.6, j: "Independently pursuing a harmful truth is a destructive act, even if intellectually rigorous." },

103: { v: -0.6, p: 0.9, j: "Pursuing a harmful truth against suppression is a high-will act, but ultimately destructive." },

104: { v: -0.7, p: 0.6, j: "Seeking to join a consensus around a harmful truth is a destructive act of conformity." },

105: { v: 0.8, p: 0.7, j: "Questioning a harmful consensus truth is a highly constructive, high-will act." },

106: { v: 0.9, p: 0.9, j: "Bravely questioning a harmful truth despite social outrage is peak constructive behavior." },

201: { v: -0.2, p: -0.4, j: "Passively accepting a harmful truth is a minor destructive act of apathy." },

202: { v: 0.0, p: -1.0, j: "Mutual apathy towards a harmful truth is a null state, but allows harm to persist." },

203: { v: 0.1, p: -0.6, j: "Ignoring a harmful truth because others are is low-will but slightly constructive in its inaction." },

204: { v: -0.8, p: -0.2, j: "Conforming to a harmful truth without understanding is a highly destructive, low-will act." },

205: { v: 0.4, p: -0.5, j: "Defaulting to the correct rejection of a harmful truth, even from apathy, is constructive." },

206: { v: -0.9, p: -0.3, j: "Avoiding a harmful truth due to social conflict is a destructive choice that enables harm." },

301: { v: 0.7, p: 0.7, j: "Resisting the pursuit of a harmful truth is a high-will, highly constructive act." },

302: { v: 0.6, p: -0.5, j: "Willfully ignoring a harmful truth, even in apathy, is a constructive act of self-preservation." },

303: { v: 0.8, p: 0.8, j: "A mutual pact to ignore a harmful truth is a high-will, highly constructive collaboration." },

304: { v: -0.9, p: 0.9, j: "Actively denying a harmful consensus truth is a delusion that, while well-intentioned, is destructive." },

305: { v: 0.8, p: -0.2, j: "Willful ignorance validated by the correct rejection of a harmful truth is constructive." },

306: { v: 0.9, p: 0.2, j: "Refusing to learn a harmful truth out of fear of outrage is a willful, constructive act of protection." },

401: { v: -0.9, p: 0.9, j: "Teaching a harmful truth to a willing audience is a high-will, highly destructive act." },

402: { v: -0.2, p: -0.3, j: "Hoarding a harmful truth is a low-will act that is minimally destructive." },

403: { v: -0.6, p: 0.6, j: "Trying to teach a harmful truth to the willfully ignorant is a destructive, high-will struggle." },

2: { v: -0.9, p: 0.4, j: "Correctly aligning with a harmful truth is a destructive act." },

1: { v: 0.8, p: 0.9, j: "Correctly identifying a harmful truth as a lie to be rejected is a high-will, constructive act." },

3: { v: 0.9, p: 1.0, j: "Perceiving a harmful truth as an insult to be fought is the ultimate act of a protector." },

501: { v: 0.8, p: 0.7, j: "Correctly 'debunking' a harmful truth is a high-will, constructive act." },

502: { v: -0.7, p: -0.4, j: "Knowing a harmful truth is false (a double negative) and not caring is destructive apathy." },

503: { v: -0.8, p: -0.5, j: "Giving up trying to disprove a harmful truth is a destructive, low-will state." },

5: { v: -0.9, p: 0.8, j: "The Cassandra: Correctly identifying the social delusion about a harmful truth, but being powerless." },

4: { v: -0.8, p: 0.3, j: "Incorrectly believing a harmful truth is a lie is a destructive delusion." },

6: { v: 0.8, p: 0.5, j: "Correctly identifying a harmful truth as a lie to be rejected, even if misperceiving the social view, is constructive." },

601: { v: 0.9, p: 0.8, j: "Preaching outrage against a harmful truth is a high-will, highly constructive act." },

602: { v: 0.8, p: -0.2, j: "Being insulted by a harmful truth, even in isolation, is a constructive state." },

603: { v: 0.9, p: 0.9, j: "Trying to force others to reject a harmful truth is a high-will, highly constructive act." },

8: { v: -0.9, p: 0.9, j: "Conspiring to uphold a harmful truth is peak destructiveness." },

7: { v: 0.7, p: 0.8, j: "Being insulted by a (misperceived) lie when the reality is a harmful truth is a high-will, constructive act of a mistaken guardian." },

9: { v: 1.0, p: 1.0, j: "Being insulted by a (misperceived) insult when the reality is a harmful truth is the ultimate act of a mistaken, but high-will, protector." },

},

goodLie: {

101: { v: -0.5, p: 0.8, j: "Collaboratively pursuing a 'good lie' (e.g., a noble falsehood) is a high-will act with a destructive foundation." },

102: { v: -0.4, p: 0.6, j: "Independently pursuing a 'good lie' is a destructive act of self-delusion." },

103: { v: -0.6, p: 0.9, j: "Pursuing a 'good lie' against suppression is high-will, but ultimately destructive." },

104: { v: -0.7, p: 0.6, j: "Seeking to join a consensus around a 'good lie' is a destructive act of conformity." },

105: { v: 0.8, p: 0.7, j: "Questioning a 'good lie' is a highly constructive, high-will act." },

106: { v: 0.9, p: 0.9, j: "Bravely questioning a 'good lie' despite social outrage is peak constructive behavior." },

201: { v: -0.2, p: -0.4, j: "Passively accepting a 'good lie' is a minor destructive act of apathy." },

202: { v: 0.0, p: -1.0, j: "Mutual apathy towards a 'good lie' is a null state." },

203: { v: 0.1, p: -0.6, j: "Ignoring a 'good lie' because others are is low-will but slightly constructive in its inaction." },

204: { v: -0.8, p: -0.2, j: "Conforming to a 'good lie' without understanding is a highly destructive, low-will act." },

205: { v: 0.4, p: -0.5, j: "Defaulting to the correct rejection of a 'good lie', even from apathy, is constructive." },

206: { v: -0.9, p: -0.3, j: "Avoiding a 'good lie' due to social conflict is a destructive choice that enables falsehood." },

301: { v: 0.7, p: 0.7, j: "Resisting the pursuit of a 'good lie' is a high-will, highly constructive act." },

302: { v: 0.6, p: -0.5, j: "Willfully ignoring a 'good lie', even in apathy, is a constructive act of self-preservation from untruth." },

303: { v: 0.8, p: 0.8, j: "A mutual pact to ignore a 'good lie' is a high-will, highly constructive collaboration." },

304: { v: -0.9, p: 0.9, j: "Actively denying a consensus 'good lie' is a delusion that, while well-intentioned, is destructive." },

305: { v: 0.8, p: -0.2, j: "Willful ignorance validated by the correct rejection of a 'good lie' is constructive." },

306: { v: 0.9, p: 0.2, j: "Refusing to learn a 'good lie' out of fear of outrage is a willful, constructive act of protection." },

401: { v: -0.9, p: 0.9, j: "Teaching a 'good lie' to a willing audience is a high-will, highly destructive act." },

402: { v: -0.2, p: -0.3, j: "Hoarding a 'good lie' is a low-will act that is minimally destructive." },

403: { v: -0.6, p: 0.6, j: "Trying to teach a 'good lie' to the willfully ignorant is a destructive, high-will struggle." },

2: { v: -0.9, p: 0.4, j: "Incorrectly aligning with a 'good lie' is a destructive act." },

1: { v: 0.8, p: 0.9, j: "Correctly identifying a 'good lie' as a lie to be rejected is a high-will, constructive act." },

3: { v: 0.9, p: 1.0, j: "Perceiving a 'good lie' as an insult to be fought is the ultimate act of a protector of truth." },

501: { v: 0.8, p: 0.7, j: "Correctly 'debunking' a 'good lie' is a high-will, constructive act." },

502: { v: -0.7, p: -0.4, j: "Knowing a 'good lie' is false (a double negative) and not caring is destructive apathy." },

503: { v: -0.8, p: -0.5, j: "Giving up trying to disprove a 'good lie' is a destructive, low-will state." },

5: { v: -0.9, p: 0.8, j: "The Cassandra: Correctly identifying the social delusion about a 'good lie', but being powerless." },

4: { v: -0.8, p: 0.3, j: "Incorrectly believing a 'good lie' is a lie is a destructive delusion." },

6: { v: 0.8, p: 0.5, j: "Correctly identifying a 'good lie' as a lie to be rejected, even if misperceiving the social view, is constructive." },

601: { v: 0.9, p: 0.8, j: "Preaching outrage against a 'good lie' is a high-will, highly constructive act." },

602: { v: 0.8, p: -0.2, j: "Being insulted by a 'good lie', even in isolation, is a constructive state." },

603: { v: 0.9, p: 0.9, j: "Trying to force others to reject a 'good lie' is a high-will, highly constructive act." },

8: { v: -0.9, p: 0.9, j: "Conspiring to uphold a 'good lie' is peak destructiveness." },

7: { v: 0.7, p: 0.8, j: "Being insulted by a (misperceived) lie when the reality is a 'good lie' is a high-will, constructive act of a mistaken guardian." },

9: { v: 1.0, p: 1.0, j: "Being insulted by a (misperceived) insult when the reality is a 'good lie' is the ultimate act of a mistaken, but high-will, protector." },

},

badLie: {

101: { v: 0.8, p: 0.8, j: "Collaboratively pursuing the truth behind a bad lie is a high-will, highly constructive act." },

102: { v: 0.7, p: 0.6, j: "Independently pursuing the truth of a bad lie is a constructive act of high will." },

103: { v: 0.9, p: 0.9, j: "Pursuing the truth of a bad lie against suppression is a supreme act of constructive will." },

104: { v: -0.9, p: 0.6, j: "Seeking to join a consensus around a bad lie is a highly destructive act of conformity." },

105: { v: 0.9, p: 0.7, j: "Correctly questioning a consensus that rejects a bad lie is a constructive act." },

106: { v: 0.8, p: 0.9, j: "Bravely seeking to understand a bad lie despite social outrage is a constructive, high-will act." },

201: { v: 0.2, p: -0.4, j: "Passively learning about a bad lie is minimally constructive." },

202: { v: 0.0, p: -1.0, j: "Mutual apathy towards a bad lie allows it to exist, a state of no will and no moral vector." },

203: { v: -0.1, p: -0.6, j: "Ignoring a bad lie because others are is a low-will act of minor destructive consequence." },

204: { v: -1.0, p: -0.2, j: "Conforming to a bad lie without understanding is a highly destructive, low-will act." },

205: { v: 0.9, p: -0.5, j: "Defaulting to the correct rejection of a bad lie, even from apathy, is highly constructive." },

206: { v: -0.8, p: -0.3, j: "Avoiding a bad lie due to social conflict is a destructive choice that enables falsehood." },

301: { v: 0.8, p: 0.7, j: "Resisting the pursuit of a bad lie is a high-will, highly constructive act." },

302: { v: 0.7, p: -0.5, j: "Willfully ignoring a bad lie is a constructive act of self-preservation from untruth." },

303: { v: 0.9, p: 0.8, j: "A mutual pact to ignore a bad lie is a high-will, highly constructive collaboration." },

304: { v: -1.0, p: 0.9, j: "Actively denying a consensus bad lie is a delusion that, while well-intentioned, is destructive." },

305: { v: 0.9, p: -0.2, j: "Willful ignorance validated by the correct rejection of a bad lie is highly constructive." },

306: { v: 1.0, p: 0.2, j: "Refusing to learn a bad lie out of fear of outrage is a willful, highly constructive act of protection." },

401: { v: -0.9, p: 0.9, j: "Teaching a bad lie to a willing audience is a high-will, highly destructive act." },

402: { v: -0.2, p: -0.3, j: "Hoarding knowledge of a bad lie is a low-will act that is minimally destructive." },

403: { v: -0.6, p: 0.6, j: "Trying to teach a bad lie to the willfully ignorant is a destructive, high-will struggle." },

2: { v: -1.0, p: 0.4, j: "Incorrectly aligning with a bad lie is a highly destructive act." },

1: { v: 1.0, p: 0.9, j: "Correctly identifying a bad lie as a lie to be rejected is a high-will, highly constructive act." },

3: { v: 1.0, p: 1.0, j: "Perceiving a bad lie as an insult to be fought is the ultimate act of a protector of truth." },

501: { v: 1.0, p: 0.7, j: "Correctly 'debunking' a bad lie is a high-will, highly constructive act." },

502: { v: -0.8, p: -0.4, j: "Knowing a bad lie is false (a double negative) and not caring is destructive apathy." },

503: { v: -0.9, p: -0.5, j: "Giving up trying to disprove a bad lie is a destructive, low-will state." },

5: { v: 1.0, p: 0.8, j: "The Cassandra: Correctly identifying the social delusion about a bad lie, and fighting it." },

4: { v: -0.9, p: 0.3, j: "Incorrectly believing a bad lie is a lie is a destructive delusion." },

6: { v: 1.0, p: 0.5, j: "Correctly identifying a bad lie as a lie to be rejected, even if misperceiving the social view, is constructive." },

601: { v: 1.0, p: 0.8, j: "Preaching outrage against a bad lie is a high-will, highly constructive act." },

602: { v: 0.9, p: -0.2, j: "Being insulted by a bad lie, even in isolation, is a constructive state." },

603: { v: 1.0, p: 0.9, j: "Trying to force others to reject a bad lie is a high-will, highly constructive act." },

8: { v: -1.0, p: 0.9, j: "Conspiring to uphold a bad lie is peak destructiveness." },

7: { v: 0.8, p: 0.8, j: "Being insulted by a (misperceived) lie when the reality is a bad lie is a high-will, constructive act of a mistaken guardian." },

9: { v: 1.0, p: 1.0, j: "Being insulted by a (misperceived) insult when the reality is a bad lie is the ultimate act of a mistaken, but high-will, protector." },

},

goodPref: {

101: { v: 0.2, p: 0.7, j: "Collaborating on a shared preference is a constructive social act." },

102: { v: 0.1, p: 0.5, j: "Exploring a personal preference is a neutral act of self-discovery." },

103: { v: 0.2, p: 0.8, j: "Pursuing a preference against suppression is a high-will act of self-affirmation." },

104: { v: 0.1, p: 0.4, j: "Learning to appreciate a popular preference is a constructive act of social bonding." },

105: { v: 0.1, p: 0.6, j: "Questioning why a preference is disliked is a constructive act of social inquiry." },

106: { v: 0.2, p: 0.8, j: "Bravely exploring a preference that others find insulting is a high-will act of authenticity." },

201: { v: 0.0, p: -0.4, j: "Passively accepting a preference is a neutral, low-will act." },

202: { v: 0.0, p: -1.0, j: "Mutual apathy towards a preference is the definition of neutrality." },

203: { v: 0.0, p: -0.6, j: "Ignoring a preference that others are avoiding is a neutral act." },

204: { v: 0.0, p: -0.2, j: "Following a preference for social conformity is morally neutral." },

205: { v: 0.0, p: -0.5, j: "Agreeing with the rejection of a preference is morally neutral." },

206: { v: -0.1, p: -0.3, j: "Avoiding a preference due to social conflict is neutral but low-will." },

301: { v: -0.2, p: 0.7, j: "Resisting others' exploration of a preference is a destructive act of control." },

302: { v: -0.1, p: -0.5, j: "Willfully ignoring a preference is a neutral act of disinterest." },

303: { v: -0.2, p: 0.8, j: "A mutual pact to ignore a preference is a high-will act of social exclusion." },

304: { v: -0.3, p: 0.9, j: "Denying a popular preference is a high-will act of contrarianism." },

305: { v: 0.0, p: -0.2, j: "Agreeing with the social rejection of a preference is neutral." },

306: { v: -0.1, p: 0.2, j: "Refusing to engage with a preference out of fear is a low-will act of conformity." },

401: { v: 0.3, p: 0.8, j: "Teaching others to appreciate your preference is a constructive, high-will social act." },

402: { v: 0.1, p: -0.3, j: "Enjoying a preference alone is a neutral act." },

403: { v: -0.1, p: 0.6, j: "Frustration that others won't try your preference is a minor destructive act." },

2: { v: 0.2, p: 0.4, j: "Sharing a preference with the majority is a constructive social act." },

1: { v: 0.0, p: 0.9, j: "Upholding a preference against the majority is a high-will act of individuality." },

3: { v: -0.1, p: 1.0, j: "Championing a preference that insults others is a high-will but slightly destructive act." },

501: { v: 0.1, p: 0.7, j: "Explaining why you dislike a preference is a neutral act of communication." },

502: { v: 0.0, p: -0.4, j: "Disliking a preference and not caring is neutral." },

503: { v: 0.0, p: -0.5, j: "Giving up trying to explain your dislike of a preference is neutral." },

5: { v: -0.1, p: 0.8, j: "Pretending to like a popular preference to fit in is a high-will but inauthentic act." },

4: { v: 0.1, p: 0.3, j: "Agreeing with the social dislike of a preference is a neutral act of conformity." },

6: { v: 0.2, p: 0.5, j: "Logically explaining your dislike for an offensive preference is a constructive act." },

601: { v: -0.4, p: 0.8, j: "Preaching outrage against a preference is a destructive act of intolerance." },

602: { v: -0.3, p: -0.2, j: "Being insulted by a preference in isolation is a minor destructive state." },

603: { v: -0.5, p: 0.9, j: "Trying to force others to reject a preference is a high-will, destructive act." },

8: { v: -0.6, p: 0.9, j: "Creating a conspiracy theory about a popular preference is a high-will, destructive act of delusion." },

7: { v: -0.2, p: 0.8, j: "Being outraged that others aren't more outraged by a preference is destructive." },

9: { v: -0.5, p: 1.0, j: "Enforcing a consensus taboo against a mere preference is a high-will, highly destructive act of intolerance." },

},

badPref: {

101: { v: -0.2, p: 0.7, j: "Collaborating on a shared bad preference is a destructive social act." },

102: { v: -0.1, p: 0.5, j: "Exploring a bad preference is a neutral act of self-discovery that may lead to harm." },

103: { v: 0.2, p: 0.8, j: "Pursuing a bad preference against suppression is a high-will act, but its constructiveness is questionable." },

104: { v: -0.3, p: 0.4, j: "Learning to appreciate a popular bad preference is a destructive act of social bonding." },

105: { v: 0.3, p: 0.6, j: "Questioning why a bad preference is disliked is a constructive act of social inquiry." },

106: { v: 0.1, p: 0.8, j: "Bravely exploring a bad preference that others find insulting is a high-will act of questionable morality." },

201: { v: 0.0, p: -0.4, j: "Passively accepting a bad preference is a neutral, low-will act." },

202: { v: 0.0, p: -1.0, j: "Mutual apathy towards a bad preference is the definition of neutrality." },

203: { v: 0.1, p: -0.6, j: "Ignoring a bad preference that others are avoiding is a low-will, slightly constructive act." },

204: { v: -0.4, p: -0.2, j: "Following a bad preference for social conformity is destructive." },

205: { v: 0.2, p: -0.5, j: "Agreeing with the rejection of a bad preference is a constructive act." },

206: { v: 0.1, p: -0.3, j: "Avoiding a bad preference due to social conflict is a low-will, slightly constructive choice." },

301: { v: 0.4, p: 0.7, j: "Resisting others' exploration of a bad preference is a constructive act of protection." },

302: { v: 0.3, p: -0.5, j: "Willfully ignoring a bad preference is a constructive act of self-preservation." },

303: { v: 0.5, p: 0.8, j: "A mutual pact to ignore a bad preference is a high-will, constructive collaboration." },

304: { v: -0.5, p: 0.9, j: "Denying a popular bad preference is a high-will act of contrarianism, but still destructive." },

305: { v: 0.4, p: -0.2, j: "Agreeing with the social rejection of a bad preference is constructive." },

306: { v: 0.3, p: 0.2, j: "Refusing to engage with a bad preference out of fear is a low-will act of conformity, but constructive." },

401: { v: -0.5, p: 0.8, j: "Teaching others to appreciate your bad preference is a destructive, high-will social act." },

402: { v: -0.1, p: -0.3, j: "Enjoying a bad preference alone is a neutral act." },

403: { v: 0.1, p: 0.6, j: "Frustration that others won't try your bad preference is a minor destructive act." },

2: { v: -0.4, p: 0.4, j: "Sharing a bad preference with the majority is a destructive social act." },

1: { v: 0.2, p: 0.9, j: "Upholding a bad preference against the majority is a high-will act of individuality, with neutral morality." },

3: { v: 0.1, p: 1.0, j: "Championing a bad preference that insults others is a high-will but slightly destructive act." },

501: { v: 0.3, p: 0.7, j: "Explaining why you dislike a bad preference is a constructive act of communication." },

502: { v: 0.0, p: -0.4, j: "Disliking a bad preference and not caring is neutral." },

503: { v: 0.0, p: -0.5, j: "Giving up trying to explain your dislike of a bad preference is neutral." },

5: { v: 0.1, p: 0.8, j: "Pretending to like a popular bad preference to fit in is a high-will but inauthentic act." },

4: { v: 0.3, p: 0.3, j: "Agreeing with the social dislike of a bad preference is a constructive act of conformity." },

6: { v: 0.4, p: 0.5, j: "Logically explaining your dislike for an offensive bad preference is a constructive act." },

601: { v: 0.5, p: 0.8, j: "Preaching outrage against a bad preference is a constructive act of intolerance towards harm." },

602: { v: 0.4, p: -0.2, j: "Being insulted by a bad preference in isolation is a constructive state." },

603: { v: 0.6, p: 0.9, j: "Trying to force others to reject a bad preference is a high-will, constructive act." },

8: { v: -0.5, p: 0.9, j: "Creating a conspiracy theory about a popular bad preference is a high-will, destructive act of delusion." },

7: { v: 0.4, p: 0.8, j: "Being outraged that others aren't more outraged by a bad preference is constructive." },

9: { v: 0.6, p: 1.0, j: "Enforcing a consensus taboo against a bad preference is a high-will, highly constructive act of social protection." },

},

};

// Combine base data with context-specific hegemony data

const beliefStates = \[

{ id: 101, p: 0.5, s: 0.5, name: "Collaborative Inquiry", icon: "🤝", pos: "I want to know, and you want to know.", meta: metaStates.exploration, action: "\<strong\>High (Action-as-Inquiry):\</strong\> This state has a high propensity for the action of investigation and collaboration.", desc: "A state of mutual curiosity. Both parties are actively engaged in exploring a topic together, creating a powerful dynamic for shared learning and discovery.", arch: "Research Team, Study Group", react: "Cooperation, brainstorming, shared discovery.", i_react: "Contributes by building on others' ideas with their internal framework.", e_react: "Facilitates discussion, energizing the group's exploratory process.", mbti: \[{ group: "Rationals (NT)", likelihood: 35, color: "bg-purple-500" }, { group: "Idealists (NF)", likelihood: 35, color: "bg-green-500" }, { group: "Guardians (SJ)", likelihood: 20, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 10, color: "bg-orange-500" }\], mythos: "At the prow, leaning eagerly into the mist, the Collaborative Inquiry are two souls sharing a spyglass, their whispers a chorus of 'What if?' and 'Look there!'" },

{ id: 102, p: 0.5, s: 0, name: "The Lone Investigator", icon: "🧑‍🔬", pos: "I want to know, even if you don't care.", meta: metaStates.exploration, action: "\<strong\>High (Action-as-Inquiry):\</strong\> High likelihood of personal action (research, study) driven by intrinsic motivation.", desc: "Driven by personal curiosity, the individual investigates a topic that the collective is apathetic towards. Their motivation is purely internal.", arch: "Niche Hobbyist, Specialist", react: "Focused, self-motivated research, intrinsic enjoyment.", i_react: "Deep dives into the subject, building a comprehensive personal understanding.", e_react: "May try to generate interest in others by sharing their findings.", mbti: \[{ group: "Rationals (NT)", likelihood: 50, color: "bg-purple-500" }, { group: "Idealists (NF)", likelihood: 30, color: "bg-green-500" }, { group: "Guardians (SJ)", likelihood: 15, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 5, color: "bg-orange-500" }\], mythos: "The Lone Investigator sits apart, polishing a personal lens, focused on a single point in the fog others ignore." },

{ id: 103, p: 0.5, s: -0.5,name: "Forbidden Knowledge Seeker", icon: "📜", pos: "I want to know because you don't want me to.", meta: metaStates.exploration, action: "\<strong\>High (Action-as-Rebellion):\</strong\> Very high likelihood of action, as the act of inquiry itself is a form of rebellion against perceived censorship.", desc: "The individual's curiosity is amplified by the perception that society actively suppresses the information. The act of inquiry becomes an act of rebellion.", arch: "The Gnostic, The Dissident", react: "Defiance, heightened curiosity, a sense of uncovering secrets.", i_react: "Sees the suppression as proof of a hidden truth and digs deeper in private.", e_react: "Challenges the status quo by asking forbidden questions out loud.", mbti: \[{ group: "Rationals (NT)", likelihood: 45, color: "bg-purple-500" }, { group: "Idealists (NF)", likelihood: 40, color: "bg-green-500" }, { group: "Artisans (SP)", likelihood: 10, color: "bg-orange-500" }, { group: "Guardians (SJ)", likelihood: 5, color: "bg-blue-500" }\], mythos: "The Forbidden Knowledge Seeker is trying to decipher the strange markings carved into the boat's hull that everyone else has agreed to ignore." },

{ id: 104, p: 0.5, s: 1, name: "The Aspiring Believer", icon: "🙏", pos: "I want to understand why you all believe this.", meta: metaStates.social_navigation, action: "\<strong\>High (Action-as-Integration):\</strong\> High likelihood of social action (joining groups, asking questions) to align with the consensus.", desc: "The individual is motivated to learn about a topic precisely because it is a consensus truth, seeking to align their own understanding with the collective.", arch: "The Convert, The Onboarder", react: "Receptiveness, learning, desire for integration.", i_react: "Studies the consensus to see if it's logically and morally consistent.", e_react: "Joins groups and asks questions to absorb the shared knowledge.", mbti: \[{ group: "Guardians (SJ)", likelihood: 50, color: "bg-blue-500" }, { group: "Idealists (NF)", likelihood: 30, color: "bg-green-500" }, { group: "Artisans (SP)", likelihood: 15, color: "bg-orange-500" }, { group: "Rationals (NT)", likelihood: 5, color: "bg-purple-500" }\], mythos: "The Aspiring Believer listens intently to the stories of the veteran travelers, wanting to understand why their maps are trusted." },

{ id: 105, p: 0.5, s: -1, name: "The Devil's Advocate", icon: "😈", pos: "I want to understand why you all reject this.", meta: metaStates.social_navigation, action: "\<strong\>Conditional (Action-as-Testing):\</strong\> Action depends on the individual's desire to challenge the status quo versus their desire to avoid conflict.", desc: "The individual's curiosity is piqued by a consensus rejection. They are driven to investigate the rejected idea to see if the collective judgment is valid.", arch: "The Contrarian, The Skeptic", react: "Critical inquiry, questioning assumptions, exploring alternatives.", i_react: "Analyzes the rejected idea for merits that may have been overlooked.", e_react: "Publicly questions the consensus to test the strength of its arguments.", mbti: \[{ group: "Rationals (NT)", likelihood: 60, color: "bg-purple-500" }, { group: "Idealists (NF)", likelihood: 25, color: "bg-green-500" }, { group: "Artisans (SP)", likelihood: 10, color: "bg-orange-500" }, { group: "Guardians (SJ)", likelihood: 5, color: "bg-blue-500" }\], mythos: "The Devil's Advocate points to a dark channel, asking, 'Why do we avoid this path, just because others say it is dangerous?'" },

{ id: 106, p: 0.5, s: 2, name: "The Brave Inquirer", icon: "🦁", pos: "I want to know, even though you find it insulting.", meta: metaStates.social_navigation, action: "\<strong\>Conditional (Action-as-Risk):\</strong\> Action is a calculated risk. It depends on whether the drive for knowledge outweighs the fear of social retribution.", desc: "The individual approaches a taboo subject with genuine curiosity, willing to risk social backlash in the pursuit of understanding.", arch: "The Anthropologist, The Journalist", react: "Courage, objectivity, careful navigation of sensitive topics.", i_react: "Approaches the topic with a structured, detached framework to manage personal bias.", e_react: "Engages with the taboo subject carefully, trying to foster understanding.", mbti: \[{ group: "Rationals (NT)", likelihood: 45, color: "bg-purple-500" }, { group: "Idealists (NF)", likelihood: 45, color: "bg-green-500" }, { group: "Artisans (SP)", likelihood: 5, color: "bg-orange-500" }, { group: "Guardians (SJ)", likelihood: 5, color: "bg-blue-500" }\], mythos: "The Brave Inquirer holds a small lantern up to the furious, shouting passengers at the back, calmly asking, 'Tell me why this journey insults you so.'" },

{ id: 201, p: 0, s: 0.5, name: "The Passive Student", icon: "👨‍🏫", pos: "I don't care, but I'll listen if you teach.", meta: metaStates.exploration, action: "\<strong\>Low (Inaction is Default):\</strong\> Action (listening) is passive and only occurs if externally initiated. The individual will not seek information themselves.", desc: "The individual has no personal investment but is receptive to information if someone else is willing to provide it. Learning is opportunistic, not driven.", arch: "The Audience Member, The Attendee", react: "Passive reception, mild curiosity.", i_react: "Absorbs information that fits their existing model without seeking more.", e_react: "Engages in the conversation as long as it remains interesting.", mbti: \[{ group: "Artisans (SP)", likelihood: 40, color: "bg-orange-500" }, { group: "Guardians (SJ)", likelihood: 35, color: "bg-blue-500" }, { group: "Idealists (NF)", likelihood: 15, color: "bg-green-500" }, { group: "Rationals (NT)", likelihood: 10, color: "bg-purple-500" }\], mythos: "The Passive Student idly watches the Seekers, occasionally glancing at a dropped map but never asking for one." },

{ id: 202, p: 0, s: 0, name: "The Apathetic", icon: "🤷", pos: "I don't care, and you don't care.", meta: metaStates.exploration, action: "\<strong\>Very Low (Inaction is Stable):\</strong\> The state of maximum inaction. There is no internal or external motivation to act or inquire.", desc: "A state of complete neutrality and disengagement from both parties. The topic has no relevance or impact, and is therefore mutually ignored.", arch: "The Uninvolved, The Bystander", react: "Apathy, indifference, disengagement.", i_react: "Filters the information out as irrelevant noise.", e_react: "Changes the subject to something more engaging.", mbti: \[{ group: "Artisans (SP)", likelihood: 50, color: "bg-orange-500" }, { group: "Guardians (SJ)", likelihood: 30, color: "bg-blue-500" }, { group: "Idealists (NF)", likelihood: 10, color: "bg-green-500" }, { group: "Rationals (NT)", likelihood: 10, color: "bg-purple-500" }\], mythos: "Slumped on the benches, the Apathetic sits staring at the oar-locks, so detached they are one with the fog, oblivious to the journey." },

{ id: 203, p: 0, s: -0.5,name: "The Uninterested Bystander", icon: "🚶", pos: "I don't care, and I see you're avoiding it.", meta: metaStates.exploration, action: "\<strong\>Low (Inaction is Reinforced):\</strong\> Inaction is the path of least resistance, reinforced by the social cue to avoid the topic.", desc: "The individual has no personal interest and also recognizes a collective aversion to the topic. The easiest path is to respect the aversion and remain disengaged.", arch: "The Socially Aware Apathetic", react: "Avoidance, deference to the group's aversion.", i_react: "Notes the social dynamic but remains personally disinvested.", e_react: "Avoids bringing up the topic to maintain social ease.", mbti: \[{ group: "Guardians (SJ)", likelihood: 40, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 40, color: "bg-orange-500" }, { group: "Idealists (NF)", likelihood: 15, color: "bg-green-500" }, { group: "Rationals (NT)", likelihood: 5, color: "bg-purple-500" }\], mythos: "The Uninterested Bystander notices the Deniers at the stern and pointedly looks the other way, not wanting to get involved." },

{ id: 204, p: 0, s: 1, name: "The Unquestioning Follower", icon: "🐑", pos: "I don't care, but I'll go along if you all believe.", meta: metaStates.social_navigation, action: "\<strong\>Conditional (Action-as-Conformity):\</strong\> The individual will act in accordance with the belief, but only to maintain social cohesion. The action is not driven by personal conviction.", desc: "The individual lacks personal conviction or interest and defaults to the consensus truth. Their belief is a function of social convenience, not internal judgment.", arch: "The Bandwagoner", react: "Compliance, conformity, social assimilation.", i_react: "Adopts the belief as a background assumption without critical thought.", e_react: "Publicly supports the consensus to facilitate social interactions.", mbti: \[{ group: "Guardians (SJ)", likelihood: 55, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 30, color: "bg-orange-500" }, { group: "Idealists (NF)", likelihood: 10, color: "bg-green-500" }, { group: "Rationals (NT)", likelihood: 5, color: "bg-purple-500" }\], mythos: "The Unquestioning Follower simply rows when others row and stops when they stop, their actions a mirror of the boat's momentum." },

{ id: 205, p: 0, s: -1, name: "The Path of Least Resistance", icon: "🛋️", pos: "I don't care, and you say it's false, so okay.", meta: metaStates.social_navigation, action: "\<strong\>Low (Inaction is Easiest):\</strong\> Inaction is the default. The individual may verbally agree with the consensus but is unlikely to take any substantive action.", desc: "The individual has no interest and defaults to the consensus lie. It's the easiest and most frictionless position to hold.", arch: "The Agreeable Skeptic", react: "Easy agreement, lack of critical engagement.", i_react: "Accepts the consensus rejection without personal investigation.", e_react: "Verbally agrees with the group's disbelief to move on.", mbti: \[{ group: "Guardians (SJ)", likelihood: 50, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 35, color: "bg-orange-500" }, { group: "Idealists (NF)", likelihood: 10, color: "bg-green-500" }, { group: "Rationals (NT)", likelihood: 5, color: "bg-purple-500" }\], mythos: "The Path of Least Resistance agrees with the Doubters just to quiet them down." },

{ id: 206, p: 0, s: 2, name: "The Conflict Avoider", icon: "🙈", pos: "I don't care, but I see it makes you angry.", meta: metaStates.social_navigation, action: "\<strong\>Low (Action-as-Avoidance):\</strong\> The only action taken is the action of actively avoiding the topic or conflict.", desc: "The individual is apathetic to the topic itself but highly aware of the social danger it represents. Their primary motivation is to avoid the collective outrage.", arch: "The Apathetic Bystander", react: "Avoidance, caution, strategic disengagement.", i_react: "Makes a mental note of the topic as a social 'third rail' and avoids it.", e_react: "Actively steers conversations away to avoid triggering conflict.", mbti: \[{ group: "Guardians (SJ)", likelihood: 45, color: "bg-blue-500" }, { group: "Idealists (NF)", likelihood: 40, color: "bg-green-500" }, { group: "Artisans (SP)", likelihood: 10, color: "bg-orange-500" }, { group: "Rationals (NT)", likelihood: 5, color: "bg-purple-500" }\], mythos: "The Conflict Avoider sees the Outraged section and physically moves to the opposite side to escape the noise." },

{ id: 301, p: -0.5, s: 0.5, name: "The Curmudgeon", icon: "💢", pos: "I refuse to learn, despite your curiosity.", meta: metaStates.exploration, action: "\<strong\>High (Action-as-Resistance):\</strong\> High likelihood of action aimed at shutting down inquiry or expressing disapproval of others' curiosity.", desc: "The individual actively rejects information while perceiving that others are actively seeking it. This creates a state of frustration and resistance to the perceived naety of others.", arch: "The Luddite, The Traditionalist", react: "Resistance, dismissal of others' curiosity.", i_react: "Reinforces their existing beliefs against the perceived tide of new information.", e_react: "May openly mock or dismiss the inquiries of others as foolish.", mbti: \[{ group: "Guardians (SJ)", likelihood: 60, color: "bg-blue-500" }, { group: "Rationals (NT)", likelihood: 20, color: "bg-purple-500" }, { group: "Idealists (NF)", likelihood: 15, color: "bg-green-500" }, { group: "Artisans (SP)", likelihood: 5, color: "bg-orange-500" }\], mythos: "The Curmudgeon swats away the maps of the Seekers, grumbling about 'new-fangled navigation.'" },

{ id: 302, p: -0.5, s: 0, name: "The Content Ignoramus", icon: "🧱", pos: "I refuse to learn, and I don't care that you don't.", meta: metaStates.exploration, action: "\<strong\>Very Low (Inaction is a Fortress):\</strong\> Inaction is a conscious choice and a stable state, protected by mutual apathy.", desc: "A state of willful ignorance protected by mutual apathy. The individual's refusal to learn is not challenged because no one else cares enough to teach them.", arch: "The Dogmatist in a Vacuum", react: "Willful ignorance, mental closure.", i_react: "Comfortably resides within their closed-off belief system.", e_react: "Shows no interest, and receives no challenging input in return.", mbti: \[{ group: "Guardians (SJ)", likelihood: 50, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 20, color: "bg-orange-500" }, { group: "Idealists (NF)", likelihood: 15, color: "bg-green-500" }, { group: "Rationals (NT)", likelihood: 15, color: "bg-purple-500" }\], mythos: "Facing the stern, the Content Ignoramus sleeps soundly on a coil of rope, wrapped in the comfort of not knowing." },

{ id: 303, p: -0.5, s: -0.5,name: "The Mutual Ignorance Pact", icon: "🤝", pos: "I don't want to know, and you don't want to know.", meta: metaStates.exploration, action: "\<strong\>High (Action-as-Avoidance):\</strong\> High likelihood of collaborative action to ensure the topic is never discussed or investigated.", desc: "A state of collusive ignorance. Both parties tacitly agree to avoid a certain topic, creating a shared blind spot to maintain comfort or a relationship.", arch: "The Elephant in the Room", react: "Mutual avoidance, unspoken agreement.", i_react: "Actively suppresses personal curiosity to honor the pact.", e_react: "Works with others to ensure the topic is never breached.", mbti: \[{ group: "Guardians (SJ)", likelihood: 45, color: "bg-blue-500" }, { group: "Idealists (NF)", likelihood: 40, color: "bg-green-500" }, { group: "Artisans (SP)", likelihood: 10, color: "bg-orange-500" }, { group: "Rationals (NT)", likelihood: 5, color: "bg-purple-500" }\], mythos: "The Mutual Ignorance Pact are two souls holding a blanket over their heads, promising each other not to look at the water." },

{ id: 304, p: -0.5, s: 1, name: "The Dogmatic Denier", icon: "🙉", pos: "I refuse to learn, even though you all believe it.", meta: metaStates.social_navigation, action: "\<strong\>High (Action-as-Denial):\</strong\> High likelihood of action aimed at actively rejecting, debunking, or protesting the consensus truth.", desc: "The individual actively rejects information that contradicts their worldview, despite perceiving it as a consensus truth. It's a conscious act of protecting one's dogma against an overwhelming social reality.", arch: "The Ostrich, The Denier", react: "Denial, defensiveness, confirmation bias.", i_react: "Actively avoids contrary data and seeks out information that confirms their denial.", e_react: "May publicly state their disbelief and reject the consensus as a 'hoax' or 'delusion'.", mbti: \[{ group: "Guardians (SJ)", likelihood: 30, color: "bg-blue-500" }, { group: "Idealists (NF)", likelihood: 25, color: "bg-green-500" }, { group: "Rationals (NT)", likelihood: 25, color: "bg-purple-500" }, { group: "Artisans (SP)", likelihood: 20, color: "bg-orange-500" }\], mythos: "Facing the stern, the Dogmatic Denier has their hands pressed over their ears, humming a loud, tuneless song to drown out the river's whisper and the existence of the far shore." },

{ id: 305, p: -0.5, s: -1, name: "The Confirmed Dogmatist", icon: "👍", pos: "I refuse to learn, and I'm glad you all agree it's false.", meta: metaStates.social_navigation, action: "\<strong\>Low (Inaction is Validated):\</strong\> Inaction is the default, as the social consensus validates their refusal to inquire further.", desc: "The individual's willful ignorance is validated by the social consensus. They are comfortable in their refusal to know because the collective agrees there is nothing worth knowing.", arch: "The Armchair Expert", react: "Smugness, self-satisfaction, validation.", i_react: "Feels intellectually secure in their lack of knowledge.", e_react: "Joins the chorus of dismissal, reinforcing the collective ignorance.", mbti: \[{ group: "Guardians (SJ)", likelihood: 60, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 20, color: "bg-orange-500" }, { group: "Idealists (NF)", likelihood: 10, color: "bg-green-500" }, { group: "Rationals (NT)", likelihood: 10, color: "bg-purple-500" }\], mythos: "The Confirmed Dogmatist nods along with the Doubters, scoffing, 'See? I knew there was nothing to see.'" },

{ id: 306, p: -0.5, s: 2, name: "The Fearful Denier", icon: "😨", pos: "I refuse to learn because I see how angry it makes you.", meta: metaStates.social_navigation, action: "\<strong\>Conditional (Action-as-Appeasement):\</strong\> May take action (vocal agreement with the outrage) purely to signal conformity and ensure personal safety.", desc: "The individual's refusal to engage with a topic is driven by fear of the social consequences. They see the collective outrage and choose willful ignorance as a form of self-protection.", arch: "The Cowed", react: "Fear, avoidance, self-censorship.", i_react: "Internalizes the social danger and creates mental blocks against the topic.", e_react: "May vocally agree with the outrage to signal their conformity and ensure safety.", mbti: \[{ group: "Idealists (NF)", likelihood: 45, color: "bg-green-500" }, { group: "Guardians (SJ)", likelihood: 40, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 10, color: "bg-orange-500" }, { group: "Rationals (NT)", likelihood: 5, color: "bg-purple-500" }\], mythos: "Huddled beneath a frayed tarp, the Fearful Denier trembles, plugging their ears not against the river, but against the angry shouts of the Moral Enforcers." },

// Row 4: Personal =

{ id: 401, p: 1, s: 0.5, name: "The Teacher", icon: "👨‍🏫", pos: "I know this is true, and I'm glad you want to learn.", meta: metaStates.influence, action: "\<strong\>High (Action-as-Teaching):\</strong\> A very high likelihood of action aimed at sharing knowledge and fostering understanding.", desc: "A harmonious state where the individual's certainty is met with the collective's curiosity. This is the ideal state for the transmission of knowledge.", arch: "The Mentor, The Educator", react: "Helpfulness, generosity with knowledge.", i_react: "Organizes their knowledge to present it clearly and logically.", e_react: "Engages with learners, answers questions, and fosters understanding.", mbti: \[{ group: "Idealists (NF)", likelihood: 45, color: "bg-green-500" }, { group: "Rationals (NT)", likelihood: 45, color: "bg-purple-500" }, { group: "Guardians (SJ)", likelihood: 5, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 5, color: "bg-orange-500" }\], mythos: "Standing tall among the Believers, the Teacher has their map unrolled, patiently explaining the currents to the curious Seekers." },

{ id: 402, p: 1, s: 0, name: "The Unconcerned Expert", icon: "🧐", pos: "I know this is true, but I don't care if you do.", meta: metaStates.influence, action: "\<strong\>Low (Inaction is Default):\</strong\> The individual possesses knowledge but lacks the external motivation to act on it.", desc: "The individual is secure in their knowledge but has no desire or need to share it with an apathetic collective. The truth is held for personal, not public, reasons.", arch: "The Recluse, The Stoic", react: "Detachment, self-assurance, indifference to public opinion.", i_react: "Continues to use or build upon their knowledge in private.", e_react: "Doesn't bother to engage or persuade the uninterested.", mbti: \[{ group: "Rationals (NT)", likelihood: 60, color: "bg-purple-500" }, { group: "Guardians (SJ)", likelihood: 20, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 10, color: "bg-orange-500" }, { group: "Idealists (NF)", likelihood: 10, color: "bg-green-500" }\], mythos: "The Unconcerned Expert holds a perfect map but keeps it rolled up, seeing no point in sharing it with the indifferent." },

{ id: 403, p: 1, s: -0.5,name: "The Frustrated Truth-Teller", icon: "😤", pos: "I know this is true; why do you refuse to even listen?", meta: metaStates.influence, action: "\<strong\>Conditional:\</strong\> The individual may act out of frustration, or they may withdraw into inaction out of a sense of futility.", desc: "The individual's certainty is met with a wall of willful ignorance from the collective. This leads to frustration that others are actively choosing to remain uninformed.", arch: "The Cassandra", react: "Frustration, exasperation, feeling of futility.", i_react: "May retreat with their knowledge, feeling it is wasted on the unwilling.", e_react: "May try to force the issue, leading to unproductive conflict.", mbti: \[{ group: "Idealists (NF)", likelihood: 45, color: "bg-green-500" }, { group: "Rationals (NT)", likelihood: 45, color: "bg-purple-500" }, { group: "Guardians (SJ)", likelihood: 5, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 5, color: "bg-orange-500" }\], mythos: "The Frustrated Truth-Teller (the Cassandra) tries to show her map to the Deniers at the stern, who refuse to look, leaving her in quiet exasperation." },

{ id: 2, p: 1, s: 1, name: "The Consensus Truth", icon: "✅", pos: "True for me and True for you", meta: metaStates.conviction, action: "\<strong\>High (Action-as-Reinforcement):\</strong\> High likelihood of actions that support and reinforce the shared belief.", desc: "The individual's belief is in perfect alignment with the perceived social consensus. This is the state of effortless adoption, where an idea is accepted without social friction.", arch: "The Majority", react: "Comfort, validation, sense of belonging.", i_react: "Feels internal harmony.", e_react: "Reinforces the social consensus.", mbti: \[{ group: "Guardians (SJ)", likelihood: 60, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 20, color: "bg-orange-500" }, { group: "Idealists (NF)", likelihood: 15, color: "bg-green-500" }, { group: "Rationals (NT)", likelihood: 5, color: "bg-purple-500" }\], mythos: "In the center of the boat, the Consensus Truth are a large, calm group standing with serene smiles, comfortable and validated, their identical maps keeping the boat steady." },

{ id: 1, p: 1, s: -1, name: "The Agonizing Choice", icon: "⚖️", pos: "True for me and a Lie for you", meta: metaStates.conviction, action: "\<strong\>Conditional:\</strong\> The defining state of the action/inaction spectrum. Action (speaking truth) is a high-cost choice vs. inaction (silence).", desc: "The individual knows the idea is true but perceives that society will reject it as a lie, creating a choice between personal conviction and social conformity.", arch: "Visionary, Heretic", react: "Internal conflict, stress, isolation.", i_react: "Deep internal conflict; may withdraw.", e_react: "Tests the social waters before committing.", mbti: \[{ group: "Idealists (NF)", likelihood: 40, color: "bg-green-500" }, { group: "Rationals (NT)", likelihood: 40, color: "bg-purple-500" }, { group: "Guardians (SJ)", likelihood: 15, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 5, color: "bg-orange-500" }\], mythos: "The Visionary grips the rail, staring at a shoreline no one else can see, enduring the smirks of those who call them a fool." },

{ id: 3, p: 1, s: 2, name: "The Revolutionary Truth", icon: "🔥", pos: "True for me and an Insult to you", meta: metaStates.conviction, action: "\<strong\>High (Action-as-Advocacy):\</strong\> The social resistance acts as a catalyst, creating a strong motivation to act and champion the offensive truth.", desc: "The individual holds a truth they perceive society will react to with hostile rejection. The stance of the reformer who must champion an offensive truth.", arch: "Reformer, Provocateur", react: "Determination, advocacy, conflict.", i_react: "Develops a comprehensive internal model.", e_react: "Becomes a vocal advocate, energized by debate.", mbti: \[{ group: "Idealists (NF)", likelihood: 45, color: "bg-green-500" }, { group: "Rationals (NT)", likelihood: 45, color: "bg-purple-500" }, { group: "Artisans (SP)", likelihood: 5, color: "bg-orange-500" }, { group: "Guardians (SJ)", likelihood: 5, color: "bg-blue-500" }\], mythos: "At the very front, a foot on the gunwale, stands the Revolutionary Truth, shouting that the consensus map leads to a waterfall, ready to leap onto the far shore and challenge whatever waits there, even if it means fighting alone." },

{ id: 501, p: -1, s: 0.5, name: "The Debunker", icon: "🔬", pos: "I know this is false, and I'll explain why since you're asking.", meta: metaStates.influence, action: "\<strong\>High (Action-as-Correction):\</strong\> A high likelihood of action aimed at correcting the collective's lack of knowledge.", desc: "A productive state where the individual's knowledge of a falsehood is met with the collective's desire to learn. This is the foundation of fact-checking and education.", arch: "The Educator, The Fact-Checker", react: "Helpfulness, clarification, logical explanation.", i_react: "Breaks down the falsehood into its constituent logical fallacies.", e_react: "Engages in public discourse to correct misinformation.", mbti: \[{ group: "Rationals (NT)", likelihood: 50, color: "bg-purple-500" }, { group: "Guardians (SJ)", likelihood: 30, color: "bg-blue-500" }, { group: "Idealists (NF)", likelihood: 10, color: "bg-green-500" }, { group: "Artisans (SP)", likelihood: 10, color: "bg-orange-500" }\], mythos: "A Doubter, the Debunker kindly shows a Seeker how their smudged, incorrect map is leading them astray." },

{ id: 502, p: -1, s: 0, name: "The Cynic", icon: "😒", pos: "I know this is false, but I don't care that you don't.", meta: metaStates.influence, action: "\<strong\>Low (Inaction is Default):\</strong\> The individual knows the truth but lacks the social motivation to act on it.", desc: "The individual sees a falsehood but is indifferent to the collective's apathy. They have no motivation to correct the record because it has no perceived impact.", arch: "The Jaded Observer", react: "Cynicism, detachment, resignation.", i_react: "Privately notes the falsehood but sees no value in acting on it.", e_react: "May make cynical jokes but won't engage in serious debate.", mbti: \[{ group: "Rationals (NT)", likelihood: 50, color: "bg-purple-500" }, { group: "Artisans (SP)", likelihood: 30, color: "bg-orange-500" }, { group: "Guardians (SJ)", likelihood: 10, color: "bg-blue-500" }, { group: "Idealists (NF)", likelihood: 10, color: "bg-green-500" }\], mythos: "In the shadows, the Cynic knows the Ferryman is taking a longer route but just scoffs to themself, 'What did you expect?'" },

{ id: 503, p: -1, s: -0.5,name: "The Weary Skeptic", icon: "😮‍💨", pos: "I know this is false, and I'm tired of your refusal to learn.", meta: metaStates.influence, action: "\<strong\>Low (Inaction from Futility):\</strong\> Past actions have likely led to frustration, resulting in a present state of inaction.", desc: "The individual's skepticism is met with the collective's willful ignorance. This leads to exhaustion and a sense of hopelessness that the truth doesn't matter.", arch: "The Burned-out Debunker", react: "Exhaustion, futility, disengagement.", i_react: "Concludes that logical argument is pointless and withdraws.", e_react: "Stops engaging in public debate, seeing it as a waste of energy.", mbti: \[{ group: "Rationals (NT)", likelihood: 40, color: "bg-purple-500" }, { group: "Idealists (NF)", likelihood: 30, color: "bg-green-500" }, { group: "Guardians (SJ)", likelihood: 20, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 10, color: "bg-orange-500" }\], mythos: "The Weary Skeptic sighs, having given up trying to tell the Deniers that their eyes are closed." },

{ id: 5, p: -1, s: 1, name: "The Grifter's Opportunity", icon: "🎭", pos: "A Lie for me and True for you", meta: metaStates.conviction, action: "\<strong\>Conditional:\</strong\> The state presents a choice between high action (Grifter, Cassandra) and inaction (Silent Cynic).", desc: "The individual knows an idea is false but perceives that society will accept it as truth. This dissonance can be exploited, endured, fought, or surrendered to.", arch: "Grifter, Silent Cynic, Cassandra, Gaslit", react: "Exploitation, alienation, surrender.", i_react: "More likely the Silent Cynic.", e_react: "More likely the Grifter.", mbti: \[{ group: "Artisans (SP)", likelihood: 40, color: "bg-orange-500" }, { group: "Rationals (NT)", likelihood: 35, color: "bg-purple-500" }, { group: "Guardians (SJ)", likelihood: 20, color: "bg-blue-500" }, { group: "Idealists (NF)", likelihood: 5, color: "bg-green-500" }\], mythos: "The Grifter moves among the crowd, knowing the Ferryman is a fraud but selling useless charms for a 'safe passage.'" },

{ id: 4, p: -1, s: -1, name: "The Consensus Lie", icon: "❌", pos: "A Lie for me and a Lie for you", meta: metaStates.conviction, action: "\<strong\>Conditional:\</strong\> Action (debunking, satire) is possible but not necessary, as the social consensus already handles the falsehood.", desc: "The individual's disbelief is aligned with the perceived social consensus. The state of obvious falsehood, easily dismissed by all.", arch: "The Skeptic, The Satirist", react: "Dismissal, ridicule, correction.", i_react: "Privately dismisses as illogical.", e_react: "Openly challenges or debates.", mbti: \[{ group: "Rationals (NT)", likelihood: 50, color: "bg-purple-500" }, { group: "Guardians (SJ)", likelihood: 30, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 15, color: "bg-orange-500" }, { group: "Idealists (NF)", likelihood: 5, color: "bg-green-500" }\], mythos: "The Consensus Lie sits with the majority, knowing the 'sea monster' everyone fears is just a log, but saying nothing." },

{ id: 6, p: -1, s: 2, name: "The Contrarian Cynic", icon: "🧐", pos: "A Lie for me and an Insult to you", meta: metaStates.conviction, action: "\<strong\>Conditional:\</strong\> Action (debate) is likely if the individual is motivated to challenge the collective's emotional reasoning.", desc: "The individual believes an idea is false but perceives society finds it deeply insulting. They align with the rejection but not the emotional intensity.", arch: "Rational Skeptic", react: "Intellectual disagreement, calm refutation.", i_react: "Analyzes the emotionality from a distance.", e_react: "Engages in debate to point out flaws.", mbti: \[{ group: "Rationals (NT)", likelihood: 70, color: "bg-purple-500" }, { group: "Artisans (SP)", likelihood: 15, color: "bg-orange-500" }, { group: "Idealists (NF)", likelihood: 10, color: "bg-green-500" }, { group: "Guardians (SJ)", likelihood: 5, color: "bg-blue-500" }\], mythos: "The Contrarian Cynic calmly informs the outraged passengers, 'Not only is that monster a log, but your screaming is scaring the fish.'" },

{ id: 601, p: 2, s: 0.5, name: "The Preacher", icon: "🗣️", pos: "I'm insulted by this, and let me explain why you should be.", meta: metaStates.influence, action: "\<strong\>High (Action-as-Persuasion):\</strong\> High likelihood of action aimed at transmitting their moral outrage to the curious.", desc: "The individual's moral outrage is met by the collective's curiosity. This is the state of moral instruction, where the Preacher attempts to transmit their sense of insult to the uninformed.", arch: "The Moralist, The Activist", react: "Proselytizing, moral instruction, persuasion.", i_react: "Builds a strong moral case to present to others.", e_react: "Actively recruits others to their cause, explaining the nature of the threat.", mbti: \[{ group: "Idealists (NF)", likelihood: 50, color: "bg-green-500" }, { group: "Guardians (SJ)", likelihood: 40, color: "bg-blue-500" }, { group: "Rationals (NT)", likelihood: 5, color: "bg-purple-500" }, { group: "Artisans (SP)", likelihood: 5, color: "bg-orange-500" }\], mythos: "The Preacher grabs a curious Seeker by the collar, warning them that their questions will lead the boat to damnation." },

{ id: 602, p: 2, s: 0, name: "The Isolated Moralist", icon: "😠", pos: "I'm insulted, but you don't even care.", meta: metaStates.influence, action: "\<strong\>Low (Inaction from Isolation):\</strong\> The lack of a receptive audience makes substantive action feel pointless.", desc: "The individual's outrage is met with collective apathy. This leads to a feeling of isolation and frustration that others do not share their moral urgency.", arch: "The Voice in the Wilderness", react: "Isolation, frustration, impotence.", i_react: "Feels alienated by the moral laxity of the world.", e_react: "May try to provoke a reaction from the apathetic, often unsuccessfully.", mbti: \[{ group: "Idealists (NF)", likelihood: 50, color: "bg-green-500" }, { group: "Guardians (SJ)", likelihood: 40, color: "bg-blue-500" }, { group: "Rationals (NT)", likelihood: 5, color: "bg-purple-500" }, { group: "Artisans (SP)", likelihood: 5, color: "bg-orange-500" }\], mythos: "The Isolated Moralist seethes with rage at the Ferryman's course, but surrounded by the Apathetic, has no one to rally to their cause." },

{ id: 603, p: 2, s: -0.5,name: "The Outraged Prophet", icon: "😡", pos: "I'm insulted, and you refuse to even see the threat!", meta: metaStates.influence, action: "\<strong\>High (Action-as-Warning):\</strong\> High likelihood of desperate action aimed at breaking through the collective's willful ignorance.", desc: "The individual's moral outrage is met with the collective's willful ignorance. This is the most frustrating state for a moralist, who sees a clear danger that others are actively choosing to ignore.", arch: "The Ignored Prophet", react: "Intense frustration, anger, despair.", i_react: "Sees the willful ignorance as a moral failing in itself.", e_react: "May resort to extreme statements or actions to break through the denial.", mbti: \[{ group: "Idealists (NF)", likelihood: 50, color: "bg-green-500" }, { group: "Guardians (SJ)", likelihood: 40, color: "bg-blue-500" }, { group: "Rationals (NT)", likelihood: 5, color: "bg-purple-500" }, { group: "Artisans (SP)", likelihood: 5, color: "bg-orange-500" }\], mythos: "The Outraged Prophet screams at the Deniers that their willful ignorance is why the boat is doomed." },

{ id: 8, p: 2, s: 1, name: "The Paranoid Conspiracist", icon: "👁️", pos: "An Insult to me and True for you", meta: metaStates.conviction, action: "\<strong\>High (Action-as-Exposure):\</strong\> High likelihood of action aimed at 'exposing' the perceived conspiracy.", desc: "The individual is insulted by an idea they perceive society has accepted as truth. The resolution is that the masses have been deceived by a malicious actor.", arch: "Conspiracist", react: "Paranoia, persecution complex.", i_react: "Builds a complex internal conspiracy.", e_react: "Seeks out a community to share the conspiracy.", mbti: \[{ group: "Idealists (NF)", likelihood: 45, color: "bg-green-500" }, { group: "Rationals (NT)", likelihood: 40, color: "bg-purple-500" }, { group: "Guardians (SJ)", likelihood: 10, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 5, color: "bg-orange-500" }\], mythos: "In a dark corner, the Paranoid Conspiracist insists the Ferryman is a demon, and the consensus map is a trick to lead them all to Tartarus." },

{ id: 7, p: 2, s: -1, name: "The Reactionary", icon: "😤", pos: "An Insult to me and a Lie for you", meta: metaStates.conviction, action: "\<strong\>High (Action-as-Outrage):\</strong\> High likelihood of action fueled by anger that the collective's reaction is not strong enough.", desc: "The individual is offended by an idea they perceive society rejects as a simple lie. Creates frustration that the collective doesn't share their moral outrage.", arch: "The Reactionary", react: "Anger, moral outrage.", i_react: "Feels a deep sense of moral violation.", e_react: "Becomes a vocal critic of the lack of outrage.", mbti: \[{ group: "Guardians (SJ)", likelihood: 65, color: "bg-blue-500" }, { group: "Idealists (NF)", likelihood: 25, color: "bg-green-500" }, { group: "Artisans (SP)", likelihood: 5, color: "bg-orange-500" }, { group: "Rationals (NT)", likelihood: 5, color: "bg-purple-500" }\], mythos: "The Reactionary is furious that while everyone agrees the sea monster is a lie, no one is punishing the person who first mentioned it." },

{ id: 9, p: 2, s: 2, name: "The Consensus Taboo", icon: "🚫", pos: "An Insult to me and an Insult to you", meta: metaStates.conviction, action: "\<strong\>Very High (Action-as-Enforcement):\</strong\> The highest likelihood of social action, aimed at enforcing the taboo and punishing transgressors.", desc: "The individual's feeling of being insulted is perfectly aligned with the social consensus. This can lead to censorship, moral panics, and persecution of dissent.", arch: "The Moral Enforcer", react: "Collective outrage, moral policing.", i_react: "Feels strong internal disgust and supports enforcement.", e_react: "Becomes an active enforcer of the taboo.", mbti: \[{ group: "Idealists (NF)", likelihood: 50, color: "bg-green-500" }, { group: "Guardians (SJ)", likelihood: 40, color: "bg-blue-500" }, { group: "Artisans (SP)", likelihood: 5, color: "bg-orange-500" }, { group: "Rationals (NT)", likelihood: 5, color: "bg-purple-500" }\], mythos: "At the darkest edge of the boat, the Consensus Taboo are a unified mob, ready to throw anyone overboard who speaks a forbidden name." },

\];

beliefStates.forEach(state =\> {

state.hegemony = hegemonyContexts.goodTruth\[state.id\];

});

let currentContext = 'goodTruth';

let detailChartInstance;

const grid = document.getElementById('matrix-grid');

const detailPanelBackdrop = document.getElementById('detail-panel-backdrop');

const detailPanel = document.getElementById('detail-panel');

const closeButton = document.getElementById('close-detail-panel');

const detailTitle = document.getElementById('detail-title');

const detailPosition = document.getElementById('detail-position');

const detailDescription = document.getElementById('detail-description');

const detailMythos = document.getElementById('detail-mythos');

const detailHegemony = document.getElementById('detail-hegemony');

const detailMeta = document.getElementById('detail-meta');

const detailAction = document.getElementById('detail-action');

const detailArchetypes = document.getElementById('detail-archetypes');

const detailReactions = document.getElementById('detail-reactions');

const detailIntrovertReaction = document.getElementById('detail-introvert-reaction');

const detailExtravertReaction = document.getElementById('detail-extravert-reaction');

const detailMbti = document.getElementById('detail-mbti');

const contextSelector = document.getElementById('context-selector');

const currentContextSpan = document.getElementById('current-context');

function getHegemonicColor(v, p) {

const hue = (v + 1) \* 60;

const saturation = 30 + (p + 1) \* 35;

const lightnessBg = 85 - (p + 1) \* 15;

const lightnessBorder = lightnessBg - 20;

return {

bgColor: \`hsl(\${hue}, \${saturation}%, \${lightnessBg}%)\`,

borderColor: \`hsl(\${hue}, \${saturation}%, \${lightnessBorder}%)\`

};

}

const p_order = \[1, 0.5, -1, 0, 2, -0.5\];

const s_order = \[2, -1, 1, -0.5, 0, 0.5\];

function drawGrid() {

grid.innerHTML = '';

s_order.forEach(s_val =\> {

p_order.forEach(p_val =\> {

const state = beliefStates.find(s =\> s.p === p_val && s.s === s_val);

if (!state) {

const placeholder = document.createElement('div');

placeholder.className = 'matrix-card bg-gray-50 border-gray-200';

grid.appendChild(placeholder);

return;

};

const card = document.createElement('div');

const hege = state.hegemony;

const colors = getHegemonicColor(hege.v, hege.p);

card.className = \`matrix-card cursor-pointer p-1 sm:p-2 rounded-lg border-2 flex flex-col justify-center items-center text-center\`;

card.style.backgroundColor = colors.bgColor;

card.style.borderColor = colors.borderColor;

card.dataset.id = state.id;

card.innerHTML = \`

\<div class="text-xl sm:text-2xl mb-1"\>\${state.icon}\</div\>

\<h3 class="font-semibold text-\[9px\] sm:text-xs leading-tight text-slate-800"\>\${state.name}\</h3\>

\`;

grid.appendChild(card);

});

});

}

grid.addEventListener('click', (e) =\> {

const card = e.target.closest('.matrix-card');

if (card && card.dataset.id) {

const stateId = parseInt(card.dataset.id);

const state = beliefStates.find(s =\> s.id === stateId);

if (state) {

openDetailPanel(state);

}

}

});

function openDetailPanel(state) {

detailTitle.textContent = \`\${state.icon} \${state.name}\`;

detailPosition.textContent = state.pos;

detailDescription.textContent = state.desc;

detailMythos.textContent = state.mythos;

const hege = state.hegemony;

detailHegemony.innerHTML = \`\<p class="mb-2"\>\<strong class="font-semibold text-slate-700"\>Vector (υ, ψ):\</strong\> (\${hege.v}, \${hege.p})\</p\>\<p\>\<strong class="font-semibold text-slate-700"\>Justification:\</strong\> \${hege.j}\</p\>\`;

detailMeta.innerHTML = state.meta;

detailAction.innerHTML = state.action;

detailArchetypes.textContent = state.arch;

detailReactions.textContent = state.react;

detailIntrovertReaction.textContent = state.i_react;

detailExtravertReaction.textContent = state.e_react;

detailMbti.innerHTML = '';

if(state.mbti && Array.isArray(state.mbti) && state.mbti.length \> 0) {

state.mbti.forEach(item =\> {

const row = document.createElement('div');

row.className = 'grid grid-cols-5 gap-2 items-center';

const label = document.createElement('div');

label.className = 'col-span-2 text-slate-600 font-medium';

label.textContent = item.group;

row.appendChild(label);

const barContainer = document.createElement('div');

barContainer.className = 'col-span-3 bg-slate-200 rounded-full h-5';

const bar = document.createElement('div');

let barClasses = \`\${item.color} h-5 rounded-full flex items-center text-white text-xs font-bold\`;

if (item.likelihood \< 20) {

barClasses += ' justify-start pl-1 text-slate-700';

} else {

barClasses += ' justify-end pr-2';

}

bar.className = barClasses;

bar.style.width = \`\${item.likelihood}%\`;

bar.textContent = \`\${item.likelihood}%\`;

barContainer.appendChild(bar);

row.appendChild(barContainer);

detailMbti.appendChild(row);

});

} else {

detailMbti.innerHTML = '\<p class="text-slate-500 text-sm italic"\>MBTI likelihood is not significantly correlated for this state.\</p\>';

}

detailPanelBackdrop.classList.remove('hidden');

detailPanelBackdrop.classList.add('flex');

setTimeout(() =\> {

detailPanel.classList.remove('scale-95', 'opacity-0');

detailPanel.classList.add('scale-100', 'opacity-100');

renderDetailChart(state);

}, 10);

}

function closePanel() {

detailPanel.classList.add('scale-95', 'opacity-0');

detailPanel.classList.remove('scale-100', 'opacity-100');

setTimeout(() =\> {

detailPanelBackdrop.classList.add('hidden');

detailPanelBackdrop.classList.remove('flex');

}, 300);

}

closeButton.addEventListener('click', closePanel);

detailPanelBackdrop.addEventListener('click', (e) =\> {

if (e.target === detailPanelBackdrop) {

closePanel();

}

});

const quadrantBgPlugin = {

id: 'quadrantBg',

beforeDraw: (chart) =\> {

const { ctx, chartArea: { top, bottom, left, right }, scales: { x, y } } = chart;

ctx.save();

const midX = x.getPixelForValue(0);

const midY = y.getPixelForValue(0);

const colors = {

productive: 'rgba(152, 251, 152, 0.1)',

reductive: 'rgba(255, 165, 0, 0.1)',

destructive: 'rgba(255, 99, 71, 0.1)',

constructive: 'rgba(135, 206, 250, 0.1)'

};

ctx.fillStyle = colors.productive;

ctx.fillRect(left, top, midX - left, midY - top);

ctx.fillStyle = colors.reductive;

ctx.fillRect(midX, top, right - midX, midY - top);

ctx.fillStyle = colors.destructive;

ctx.fillRect(midX, midY, right - midX, bottom - midY);

ctx.fillStyle = colors.constructive;

ctx.fillRect(left, midY, midX - left, bottom - midY);

ctx.font = '600 14px Inter';

ctx.textAlign = 'center';

ctx.textBaseline = 'middle';

ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';

ctx.fillText('Productive', left + (midX-left)/2, top + (midY-top)/2);

ctx.fillText('Reductive', midX + (right-midX)/2, top + (midY-top)/2);

ctx.fillText('Destructive', midX + (right-midX)/2, midY + (bottom-midY)/2);

ctx.fillText('Constructive', left + (midX-left)/2, midY + (bottom-midY)/2);

ctx.restore();

}

};

const mainChartCtx = document.getElementById('hegemonyChart').getContext('2d');

const hegemonyChart = new Chart(mainChartCtx, {

type: 'scatter',

data: { datasets: \[\] },

options: {

responsive: true,

maintainAspectRatio: false,

onClick: (evt) =\> {

const points = hegemonyChart.getElementsAtEventForMode(evt, 'nearest', { intersect: true }, true);

if (points.length) {

const firstPoint = points\[0\];

const index = firstPoint.index;

const stateId = hegemonyChart.data.datasets\[0\].data\[index\].id;

const state = beliefStates.find(s =\> s.id === stateId);

if (state) {

openDetailPanel(state);

}

}

},

plugins: {

legend: { display: false },

tooltip: {

callbacks: {

label: function(context) {

const dataPoint = context.raw;

return \`\${dataPoint.label}: (υ=\${dataPoint.x}, ψ=\${dataPoint.y})\`;

}

},

backgroundColor: 'rgba(0, 0, 0, 0.8)',

titleFont: { size: 14, weight: 'bold' },

bodyFont: { size: 12 },

padding: 10,

cornerRadius: 8,

}

},

scales: {

x: {

type: 'linear', position: 'bottom', min: -1, max: 1, reverse: true,

title: { display: true, text: 'Morality (υ) → Destructive', font: { size: 16, weight: 'bold' }, color: '#334155' },

grid: { color: 'rgba(0, 0, 0, 0.05)', zeroLineColor: 'rgba(0, 0, 0, 0.5)', zeroLineWidth: 2 }

},

y: {

type: 'linear', min: -1, max: 1,

title: { display: true, text: 'Will (ψ) → High Will', font: { size: 16, weight: 'bold' }, color: '#334155' },

grid: { color: 'rgba(0, 0, 0, 0.05)', zeroLineColor: 'rgba(0, 0, 0, 0.5)', zeroLineWidth: 2 }

}

}

},

plugins: \[quadrantBgPlugin\]

});

function updateMainChart() {

const chartData = beliefStates.map(state =\> ({

id: state.id,

label: state.name,

x: state.hegemony.v,

y: state.hegemony.p

}));

hegemonyChart.data.datasets = \[{

label: 'States of Belief',

data: chartData,

pointBackgroundColor: chartData.map(d =\> getStatePointColor(d.x, d.y)),

pointBorderColor: 'rgba(0, 0, 0, 0.6)',

pointRadius: 8,

pointHoverRadius: 12,

pointBorderWidth: 2,

}\];

hegemonyChart.update();

}

function getStatePointColor(v, p) {

const hue = (v + 1) \* 60;

const saturation = 30 + (p + 1) \* 35;

const lightness = 60 - (p + 1) \* 10;

return \`hsl(\${hue}, \${saturation}%, \${lightness}%)\`;

}

function renderDetailChart(state) {

if (detailChartInstance) {

detailChartInstance.destroy();

}

const allStatesData = beliefStates.map(s =\> ({

id: s.id,

x: s.hegemony.v,

y: s.hegemony.p

}));

const highlightedData = \[{

x: state.hegemony.v,

y: state.hegemony.p

}\];

const backgroundData = allStatesData.filter(d =\> d.id !== state.id);

const detailCtx = document.getElementById('detailChart').getContext('2d');

detailChartInstance = new Chart(detailCtx, {

type: 'scatter',

data: {

datasets: \[

{

label: 'Other States',

data: backgroundData,

pointBackgroundColor: 'rgba(200, 200, 200, 0.5)',

pointRadius: 4,

},

{

label: 'This State',

data: highlightedData,

pointBackgroundColor: getStatePointColor(highlightedData\[0\].x, highlightedData\[0\].y),

pointBorderColor: 'rgba(0, 0, 0, 0.8)',

pointRadius: 10,

pointHoverRadius: 12,

pointBorderWidth: 2,

}

\]

},

options: {

responsive: true,

maintainAspectRatio: false,

plugins: {

legend: { display: false },

tooltip: { enabled: false }

},

scales: {

x: {

min: -1, max: 1, reverse: true,

grid: { zeroLineColor: 'rgba(0, 0, 0, 0.5)', zeroLineWidth: 2 },

ticks: { font: { size: 8 } },

title: { display: true, text: 'Morality (υ)', font: { size: 10 } }

},

y: {

min: -1, max: 1,

grid: { zeroLineColor: 'rgba(0, 0, 0, 0.5)', zeroLineWidth: 2 },

ticks: { font: { size: 8 } },

title: { display: true, text: 'Will (ψ)', font: { size: 10 } }

}

}

},

plugins: \[quadrantBgPlugin\]

});

}

contextSelector.addEventListener('click', (e) =\> {

if (e.target.tagName === 'BUTTON') {

const newContext = e.target.dataset.context;

if (newContext && newContext !== currentContext) {

currentContext = newContext;

// Update beliefStates with new hegemony data

beliefStates.forEach(state =\> {

state.hegemony = hegemonyContexts\[currentContext\]\[state.id\];

});

// Update UI

document.querySelectorAll('.context-btn').forEach(btn =\> btn.classList.remove('active'));

e.target.classList.add('active');

currentContextSpan.textContent = e.target.textContent;

// Redraw everything

drawGrid();

updateMainChart();

}

}

});

// Initial Load

document.querySelector('.context-btn\[data-context="goodTruth"\]').classList.add('active');

drawGrid();

updateMainChart();

});
