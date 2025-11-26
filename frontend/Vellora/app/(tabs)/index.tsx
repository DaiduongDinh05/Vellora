import { Text, View, ScrollView, TouchableOpacity } from "react-native";
import { Link, useRouter } from "expo-router";
import { SafeAreaView, useSafeAreaInsets } from "react-native-safe-area-context";
import { getProviderAuthorizeUrl, login } from "../services/auth";
// import Tracking from "../components/tracking";

export default function Index() {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  

  return (

    <View style= {{ flex: 1 }}>
      <View className="bg-testWhite flex-1">

        <ScrollView
          showsVerticalScrollIndicator={false}
          contentContainerStyle={{ paddingBottom: 100 }}
        >

          {/* purple header */}
          <View className="bg-primaryPurple w-full pb-10">

            <View style={{ paddingTop: insets.top + 20, paddingHorizontal: 25 }}>
              <Text className="text-5xl text-textWhite font-bold">Welcome back,</Text>

            </View>

          </View>
        </ScrollView>
      </View>
    </View>
    // <SafeAreaView className="flex-1 justify-start p-[25px]"
    // >
    //   <View className="bg-primaryPurple">
    //     <Text className="text-5xl text-primaryPurple font-bold">Welcome back,</Text>
    //   </View>
    //   <Link href="../tracking">Live track a trip</Link>
    //   <Link href="../manualLogScreen">Manually log a trip</Link>
    //   <Link href="../trackingTest"></Link>
    //   {/* <Tracking></Tracking> */}
    // </SafeAreaView>
  );
}
