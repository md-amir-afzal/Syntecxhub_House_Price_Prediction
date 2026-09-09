import React, { useState } from 'react';
import { View, Text, TextInput, Pressable, StyleSheet, SafeAreaView, ScrollView, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { apiFetch } from '../lib/api';

export default function Chat() {
  const router = useRouter();
  const [q, setQ] = useState('');
  const [msgs, setMsgs] = useState<{role:string,text:string}[]>([{role:'ai',text:'Namaste! Main MediCare AI hoon. Aap Hindi, English ya Hinglish mein apni problem bata sakte hain. Main diagnosis nahi karunga; pehle zaroori details samajhne mein help karunga.'}]);
  const [loading, setLoading] = useState(false);
  async function send(){
    const message=q.trim(); if(!message||loading)return; setQ(''); setMsgs(m=>[...m,{role:'user',text:message}]); setLoading(true);
    try { const res=await apiFetch('/api/v1/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message,language:'hinglish'})}); const data=await res.json(); if(res.status===401){router.replace('/auth');return} if(!res.ok)throw new Error(data.detail||'Unable to continue'); setMsgs(m=>[...m,{role:'ai',text:data.reply}]); if(data.emergency) router.push('/emergency'); }
    catch { setMsgs(m=>[...m,{role:'ai',text:'Internet connection check karke dobara try karein. Agar symptoms serious hain, AI ka wait mat karein—professional medical care lein.'}]); }
    finally{setLoading(false)}
  }
  return <SafeAreaView style={s.safe}><View style={s.head}><Text style={s.h}>Talk to MediCare AI</Text><Text style={s.sub}>Hindi • English • Hinglish</Text></View><ScrollView contentContainerStyle={s.c}>{msgs.map((m,i)=><View key={i} style={[s.msg,m.role==='user'&&s.user]}><Text style={s.t}>{m.text}</Text></View>)}{loading&&<ActivityIndicator color="#176B61"/>}</ScrollView><View style={s.bar}><TextInput value={q} onChangeText={setQ} placeholder="Apni problem yahan likhein…" style={s.input}/><Pressable onPress={send} style={s.send}><Text style={s.sendT}>➤</Text></Pressable></View></SafeAreaView>
}
const s=StyleSheet.create({safe:{flex:1,backgroundColor:'#F6FBFA'},head:{padding:18,paddingBottom:8},h:{fontSize:26,fontWeight:'900',color:'#123D38'},sub:{fontSize:13,color:'#58736F',marginTop:3},c:{padding:18,paddingBottom:100},msg:{maxWidth:'90%',alignSelf:'flex-start',backgroundColor:'#fff',borderRadius:18,padding:14,marginBottom:10,borderWidth:1,borderColor:'#D9EAE7'},user:{alignSelf:'flex-end',backgroundColor:'#E6F5F1'},t:{fontSize:15,lineHeight:22,color:'#294A46'},bar:{position:'absolute',left:0,right:0,bottom:0,padding:12,backgroundColor:'#fff',flexDirection:'row',gap:8,borderTopWidth:1,borderColor:'#D9EAE7'},input:{flex:1,borderWidth:1,borderColor:'#C9DEDA',borderRadius:15,paddingHorizontal:14,fontSize:15,backgroundColor:'#fff'},send:{width:52,height:52,borderRadius:15,backgroundColor:'#176B61',alignItems:'center',justifyContent:'center'},sendT:{color:'#fff',fontSize:22}});
