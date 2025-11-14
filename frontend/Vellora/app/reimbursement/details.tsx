import { View, Text, Pressable, SafeAreaView } from "react-native";
import { useLocalSearchParams, router } from "expo-router";
import { rateStyles } from "../styles/ReimbursementStyles";

export default function CustomRateDetailsPage() {
  const params = useLocalSearchParams();
  const raw = params?.data ? String(params.data) : "";
  const rate = raw ? JSON.parse(raw) : null;

  if (!rate) {
    return (
      <SafeAreaView style={rateStyles.safe}>
        <Text style={{ marginTop: 40, textAlign: "center" }}>No rate found.</Text>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={rateStyles.safe}>
      <View style={rateStyles.screenContainer}>
        <View style={rateStyles.headerRow}>
          <Pressable onPress={() => router.back()}>
            <Text style={rateStyles.backArrow}>{"<"}</Text>
          </Pressable>
          <Text style={rateStyles.headerTitle}>{rate.name}</Text>
        </View>

        {rate.description ? (
          <Text style={[rateStyles.paragraph, { marginTop: 12 }]}>
            {rate.description}
          </Text>
        ) : null}

        <Text
          style={{
            marginTop: 30,
            marginBottom: 8,
            fontSize: 14,
            fontWeight: "700",
            color: "#4F46E5",
          }}
        >
          RATES
        </Text>

        <View
          style={{
            backgroundColor: "white",
            borderRadius: 12,
            overflow: "hidden",
          }}
        >
          {rate.categories.map((c: any, i: number) => (
            <View
              key={c.id}
              style={{
                flexDirection: "row",
                justifyContent: "space-between",
                paddingVertical: 14,
                paddingHorizontal: 18,
                borderBottomWidth:
                  i < rate.categories.length - 1 ? 1 : 0,
                borderColor: "#E5E7EB",
              }}
            >
              <Text style={{ fontSize: 16 }}>{c.name}</Text>
              <Text style={{ fontSize: 16 }}>${c.rate}</Text>
            </View>
          ))}
        </View>
      </View>
    </SafeAreaView>
  );
}
