import React, { useState } from "react";
import { View, Text, StyleSheet, ScrollView } from "react-native";
import ScreenLayout from "../components/ScreenLayout";
import Button from "../components/Button";
import MonthYearDropdown from "../components/MonthYearDropdown";
import { reportStyles } from "../styles/ReportStyles";

const sampleData = [
  { label: "Personal", value: 12, color: "#F97316" },
  { label: "Work", value: 28, color: "#4F46E5" },
  { label: "Client", value: 7, color: "#10B981" },
  { label: "Other", value: 16, color: "#EF4444" },
  { label: "Travel", value: 21, color: "#F59E0B" },
];

export default function AnalyticsPage() {
  const [currentDate, setCurrentDate] = useState<Date>(new Date());

  const maxValue = Math.max(...sampleData.map((d) => d.value), 1);

  return (
    <ScreenLayout
      footer={
        <View>
          <Button title="Generate Reports" onPress={() => {}} className="mt-3 py-4 px-5" />
        </View>
      }>
      <ScrollView contentContainerStyle={{ padding: 24 }}>
        <Text style={reportStyles.title}>Analytics</Text>

        <Text style={reportStyles.sectionLabel}>Select Month</Text>
        <View style={{ marginBottom: 18 }}>
          <MonthYearDropdown currentDate={currentDate} onDateChange={setCurrentDate} />
        </View>

        <View style={styles.card}>
          <Text style={[reportStyles.sectionLabel, { marginBottom: 12 }]}>Trips by Category</Text>

          <View style={styles.chartContainer}>
            <View style={styles.barsRow}>
              {sampleData.map((d) => {
                const height = (d.value / maxValue) * 180; // px
                return (
                  <View key={d.label} style={styles.barWrapper}>
                    <View style={[styles.bar, { height, backgroundColor: d.color }]} />
                    <Text style={styles.barLabel}>{d.label}</Text>
                    <Text style={styles.barValue}>{d.value}</Text>
                  </View>
                );
              })}
            </View>
          </View>
        </View>

        <View style={{ height: 48 }} />
      </ScrollView>
    </ScreenLayout>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: "white",
    padding: 20,
    borderRadius: 16,
    shadowColor: "#000",
    shadowOpacity: 0.08,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 2 },
    elevation: 2,
    marginBottom: 12,
  },
  chartContainer: {
    paddingTop: 12,
  },
  barsRow: {
    flexDirection: "row",
    alignItems: "flex-end",
    justifyContent: "space-between",
    height: 220,
  },
  barWrapper: {
    flex: 1,
    alignItems: "center",
    marginHorizontal: 6,
  },
  bar: {
    width: 28,
    borderRadius: 6,
  },
  barLabel: {
    marginTop: 8,
    fontSize: 12,
    color: "#374151",
    textAlign: "center",
  },
  barValue: {
    marginTop: 4,
    fontSize: 12,
    fontWeight: "600",
    color: "#111827",
  },
});
