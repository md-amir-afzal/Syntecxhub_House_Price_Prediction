import AsyncStorage from '@react-native-async-storage/async-storage';
export const API = process.env.EXPO_PUBLIC_API_URL || 'http://10.0.2.2:8000';
export const TOKEN_KEY = 'medicare_access_token';
export async function getToken(){ return AsyncStorage.getItem(TOKEN_KEY); }
export async function apiFetch(path:string, init:RequestInit={}){
  const token=await getToken();
  const headers=new Headers(init.headers || {});
  if(token) headers.set('Authorization',`Bearer ${token}`);
  return fetch(`${API}${path}`,{...init,headers});
}
