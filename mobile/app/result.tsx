import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, ScrollView, Pressable, Linking, Alert } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';

const riskIcon: Record<string, string> = {
  'Low Risk': '🟢', 'Moderate Risk': '🟡', 'High Risk': '🟠', Emergency: '🔴'
};

export default function Result() {
  const p = useLocalSearchParams();
  const r = useRouter();
  let d: any = {};
  try { d = JSON.parse(String(p.data)); } catch { d = { risk_level: 'Moderate Risk', summary: 'Unable to read assessment.' }; }
  const emergency = Boolean(d.emergency);
  return <SafeAreaView style={s.safe}><ScrollView contentContainerStyle={s.c}>
    <Text style={s.eyebrow}>MediCare AI</Text>
    <Text style={s.h}>Your Health Assessment</Text>
    {emergency && <View style={s.em}><Text style={s.emh}>🔴 MEDICAL EMERGENCY</Text><Text style={s.emt}>{d.recommended_action}</Text><Pressable style={s.emBtn} onPress={() => r.push('/emergency')}><Text style={s.emBtnT}>View Emergency Instructions</Text></Pressable></View>}
    <View style={s.risk}><Text style={s.riskIcon}>{riskIcon[d.risk_level] || '🟡'}</Text><View><Text style={s.riskLabel}>Risk Level</Text><Text style={s.riskValue}>{d.risk_level || 'Needs review'}</Text></View></View>
    <Section title="1. Symptom Summary"><Text style={s.body}>{d.summary || 'No summary available.'}</Text></Section>
    <Section title="2. Possible Causes">{(d.possible_conditions || []).map((x: string, i: number) => <Text key={i} style={s.bullet}>• {x}</Text>)}<Text style={s.small}>These are possibilities, not a diagnosis.</Text></Section>
    <Section title="3. Risk & Warning Signs"><Text style={s.body}>{(d.red_flags || []).length ? d.red_flags.join(', ') : 'No emergency red flags were identified by the screening layer.'}</Text></Section>
    <Section title="4. Recommended Action"><Text style={s.body}>{d.recommended_action}</Text></Section>
    <Section title="Self-care">{(d.self_care || []).map((x: string, i: number) => <Text key={i} style={s.bullet}>• {x}</Text>)}</Section>
    {(d.otc_information || []).length > 0 && <Section title="OTC information"><Text style={s.body}>{d.otc_information.join('\n')}</Text><Text style={s.warning}>⚠️ Confirm with a doctor/pharmacist before taking any medicine.</Text></Section>}
    {(d.follow_up_questions || []).length > 0 && <Section title="Questions that may help">{d.follow_up_questions.map((x: string, i: number) => <Text key={i} style={s.bullet}>• {x}</Text>)}</Section>}
    <Pressable style={s.primary} onPress={() => r.replace('/assessment')}><Text style={s.primaryT}>Start New Assessment</Text></Pressable>
    <Pressable style={s.secondary} onPress={() => r.push('/chat')}><Text style={s.secondaryT}>Ask MediCare AI a Question</Text></Pressable><Pressable style={s.secondary} onPress={async()=>{try{await Linking.openURL('https://www.google.com/maps/search/?api=1&query=doctor+near+me')}catch{Alert.alert('Unable to open maps','Please use your maps app to find a nearby doctor.')}}}><Text style={s.secondaryT}>📍 Find a Doctor Near Me</Text></Pressable>
    <Text style={s.disc}>⚠️ MediCare AI is an educational and triage tool, not a doctor. It cannot diagnose disease or prescribe treatment. For emergencies or serious symptoms, seek immediate professional medical care.</Text>
  </ScrollView></SafeAreaView>;
}
function Section({ title, children }: any) { return <View style={s.sec}><Text style={s.sh}>{title}</Text>{children}</View>; }
const s = StyleSheet.create({safe:{flex:1,backgroundColor:'#F6FBFA'},c:{padding:20,paddingBottom:44},eyebrow:{fontSize:13,fontWeight:'800',color:'#176B61'},h:{fontSize:28,fontWeight:'900',color:'#123D38',marginBottom:14},risk:{backgroundColor:'#fff',borderRadius:20,padding:18,flexDirection:'row',alignItems:'center',gap:14,borderWidth:1,borderColor:'#D9EAE7'},riskIcon:{fontSize:36},riskLabel:{fontSize:12,color:'#58736F'},riskValue:{fontSize:21,fontWeight:'800',color:'#123D38',marginTop:2},sec:{backgroundColor:'#fff',borderRadius:18,padding:17,marginTop:12,borderWidth:1,borderColor:'#D9EAE7'},sh:{fontSize:17,fontWeight:'800',color:'#176B61',marginBottom:9},body:{fontSize:15,lineHeight:22,color:'#294A46'},bullet:{fontSize:14,lineHeight:23,color:'#294A46',marginBottom:3},small:{fontSize:12,lineHeight:18,color:'#6B7775',marginTop:8},warning:{fontSize:13,lineHeight:19,color:'#705B20',backgroundColor:'#FFF8E6',padding:11,borderRadius:10,marginTop:10},em:{backgroundColor:'#FFF0EE',borderWidth:1,borderColor:'#E85D4A',borderRadius:18,padding:18,marginBottom:12},emh:{fontSize:18,fontWeight:'900',color:'#A8281D'},emt:{fontSize:14,lineHeight:21,color:'#5A2824',marginTop:7},emBtn:{backgroundColor:'#A8281D',padding:14,borderRadius:12,marginTop:12,alignItems:'center'},emBtnT:{color:'#fff',fontWeight:'800'},primary:{height:56,backgroundColor:'#176B61',borderRadius:16,alignItems:'center',justifyContent:'center',marginTop:16},primaryT:{color:'#fff',fontWeight:'800',fontSize:16},secondary:{height:54,backgroundColor:'#fff',borderRadius:16,alignItems:'center',justifyContent:'center',marginTop:10,borderWidth:1,borderColor:'#BFD9D5'},secondaryT:{color:'#176B61',fontWeight:'800',fontSize:15},disc:{fontSize:12,lineHeight:18,color:'#6E5B28',backgroundColor:'#FFF8E6',padding:13,borderRadius:13,marginTop:14}});
