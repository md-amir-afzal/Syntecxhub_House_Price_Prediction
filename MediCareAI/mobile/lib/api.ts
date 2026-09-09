import AsyncStorage from '@react-native-async-storage/async-storage';

export const API = process.env.EXPO_PUBLIC_API_URL || 'http://10.0.2.2:8000';
const TOKEN_KEY = 'medicare_access_token';

export async function getToken(){ return AsyncStorage.getItem(TOKEN_KEY); }
export async function setToken(token:string){ await AsyncStorage.setItem(TOKEN_KEY, token); }
export async function clearToken(){ await AsyncStorage.removeItem(TOKEN_KEY); }

export async function api(path:string, options:RequestInit = {}){
  const token=await getToken();
  const headers:any={...(options.headers||{})};
  if(!(options.body instanceof FormData)) headers['Content-Type']='application/json';
  if(token) headers.Authorization=`Bearer ${token}`;
  const res=await fetch(`${API}${path}`,{...options,headers});
  let data:any={}; try{data=await res.json();}catch{}
  if(!res.ok) throw new Error(data.detail || 'Something went wrong.');
  return data;
}
