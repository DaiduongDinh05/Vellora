import { View, Text, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { Image } from 'expo-image';
import { FontAwesome } from '@expo/vector-icons';

export default function MyProfile() {
  const router = useRouter();

  return (
    <View className="flex-1 bg-gray-60">
        
        <View className="bg-white px-10 py-20 mx-3 mt-3 rounded-3xl">
          <View className="flex-row items-center">
            <View 
              style={{width: 120, height: 120, borderWidth: 0}}
              className="items-center justify-center mr-10"
            >
              <Image 
                source={require('../assets/placeholderProfile.svg')}
                contentFit="cover"
                style={{width: 200, height: 125, borderRadius: 55}}
              />
            </View>
            
            <View className="flex-1">
              <Text 
                style={{
                  fontSize: 23,
                  fontFamily: 'Inter',
                  fontWeight: 'bold',
                  color: '#404CCF',
                  marginBottom: 8
                }}
              >
                John Doe
              </Text>
              <View className="flex-row mb-4">
                <Text className="text-black mr-6 font-bold">34 trips</Text>
                <Text className="text-black font-bold">3 scheduled</Text>
              </View>
              
              <TouchableOpacity 
                style={{
                  backgroundColor: '#898989',
                  borderRadius: 12,
                  paddingHorizontal: 45,
                  paddingVertical: 8,
                  alignSelf: 'flex-start'
                }}>
                <Text className="text-white font-medium">Edit profile</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>

        
        <Text 
          style={{
            fontSize: 14,
            fontFamily: 'Inter',
            fontWeight: 'bold',
            color: '#404CCF',
            marginTop: 20,
            marginLeft: 30
          }}>PERSONALIZATION</Text>

        <View className="bg-white mt-3 mx-3 rounded-3xl">
          <View className="mt-1">
            
            <TouchableOpacity 
              className="bg-white px-6 py-4 flex-row items-center justify-between border-b border-gray-100 rounded-3xl mb-1"
              onPress={() => router.push('/reimbursement')}
            >
              <View className="flex-row items-center">
                <FontAwesome name="dollar" size={22} color="black" className="mr-3 ml-2" />
                <Text className="text-black text-base ml-3">Reimbursement rate</Text>
              </View>
              <FontAwesome name="chevron-right" size={16} color="black" />
            </TouchableOpacity>

            <TouchableOpacity className="bg-white px-6 py-4 flex-row items-center justify-between rounded-3xl mb-1">
              <View className="flex-row items-center">
                <FontAwesome name="car" size={18} color="black" className="mr-3 ml-2" />
                <Text className="text-black text-base ml-3">Vehicles</Text>
              </View>
              <FontAwesome name="chevron-right" size={16} color="black" />
            </TouchableOpacity>

          </View>
        </View>

        <Text 
          style={{
            fontSize: 14,
            fontFamily: 'Inter',
            fontWeight: 'bold',
            color: '#404CCF',
            marginTop: 20,
            marginLeft: 30
          }}>ACCOUNT</Text>

        <View className="bg-white mt-3 mx-3 rounded-3xl">
          <View className="mt-1">
            
            <TouchableOpacity className="bg-white px-6 py-4 flex-row items-center justify-between border-b border-gray-100 rounded-3xl mb-1">
              <View className="flex-row items-center">
                <Text className="text-black text-base ml-3"></Text>
              </View>
            </TouchableOpacity>

            <TouchableOpacity className="bg-white px-6 py-4 flex-row items-center justify-between rounded-3xl mb-1">
              <View className="flex-row items-center">
                <Text className="text-black text-base ml-3"></Text>
              </View>
            </TouchableOpacity>

          </View>
        </View>

    </View>
  );
}