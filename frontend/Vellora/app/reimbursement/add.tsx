import { useState } from "react";
import {
  View,
  Text,
  TextInput,
  Pressable,
  SafeAreaView,
  KeyboardAvoidingView,
  Platform,
  Modal,
  FlatList
} from "react-native";
import { router } from "expo-router";
import { rateStyles }from "../styles/ReimbursementStyles";
import CurrencyInput from "../components/CurrencyInput";
import { Category, CustomRate } from "./index";

export default function AddCustomRatePage() {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [year, setYear] = useState("");
  const [yearPickerVisible, setYearPickerVisible] = useState(false);

  const [categories, setCategories] = useState<Category[]>([]);
  const [isAddingCategory, setIsAddingCategory] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState("");
  const [newCategoryRate, setNewCategoryRate] = useState("0.00");
  const [errors, setErrors] = useState("");

  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: currentYear - 1999 + 2 }, (_, i) => `${2000 + i}`);

  const validateBeforeSave = () => {
    if (!name.trim()) return setErrors("Name is required.");
    if (!year.trim()) return setErrors("Year is required.");
    if (categories.length === 0) return setErrors("You must add at least one category.");
    for (const c of categories) {
      if (!c.name.trim()) return setErrors("Category names cannot be empty.");
      if (!c.rate.trim()) return setErrors("Category rates cannot be empty.");
    }
    setErrors("");
    return true;
  };

  const addNewCategory = () => {
    const trimmed = newCategoryName.trim();
    if (!trimmed) {
      setIsAddingCategory(false);
      return;
    }
    const next: Category = {
      id: `${Date.now()}`,
      name: trimmed,
      rate: newCategoryRate || "0.00"
    };
    setCategories((prev) => [...prev, next]);
    setIsAddingCategory(false);
    setNewCategoryName("");
    setNewCategoryRate("0.00");
    setErrors("");
  };

  const deleteCategory = (id: string) => {
    setCategories((prev) => prev.filter((c) => c.id !== id));
  };

  const updateCategoryRate = (id: string, val: string) => {
    setCategories((prev) =>
      prev.map((c) => (c.id === id ? { ...c, rate: val } : c))
    );
  };

  const handleSave = () => {
    if (!validateBeforeSave()) return;

    const payload: CustomRate = {
      id: `${Date.now()}`,
      name,
      description,
      year,
      categories
    };

    const encoded = encodeURIComponent(JSON.stringify(payload));

    router.push(`/reimbursement?newRate=${encoded}`);
  };

  return (
    <SafeAreaView style={rateStyles.safe}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === "ios" ? "padding" : undefined}
      >
        <View style={rateStyles.fullScreenWhite}>
          <View style={rateStyles.formHeaderRow}>
            <Pressable onPress={() => router.back()} style={rateStyles.closeCircle}>
              <Text style={rateStyles.closeText}>×</Text>
            </Pressable>
            <Text style={rateStyles.formTitle}>Add custom rate</Text>
          </View>

          {errors ? (
            <Text style={{ color: "red", marginBottom: 8 }}>{errors}</Text>
          ) : null}

          <View style={rateStyles.formFieldGroup}>
            <Text style={rateStyles.formLabel}>Name</Text>
            <TextInput
              style={rateStyles.formInput}
              placeholder="Enter a name"
              placeholderTextColor="#9CA3AF"
              value={name}
              onChangeText={setName}
            />
          </View>

          <View style={rateStyles.formFieldGroup}>
            <Text style={rateStyles.formLabel}>Description</Text>
            <TextInput
              style={rateStyles.formInput}
              placeholder="Enter a description"
              placeholderTextColor="#9CA3AF"
              value={description}
              onChangeText={setDescription}
            />
          </View>

          <View style={rateStyles.formFieldGroup}>
            <Text style={rateStyles.formLabel}>Year</Text>
            <Pressable
              style={[rateStyles.formInput, { width: 120, justifyContent: "center" }]}
              onPress={() => setYearPickerVisible(true)}
            >
              <Text style={{ color: year ? "#000" : "#9CA3AF" }}>
                {year || "Select year"}
              </Text>
            </Pressable>
          </View>

          <Modal visible={yearPickerVisible} transparent animationType="fade">
            <View
              style={{
                flex: 1,
                backgroundColor: "rgba(0,0,0,0.4)",
                justifyContent: "center",
                alignItems: "center"
              }}
            >
              <View
                style={{
                  width: "80%",
                  backgroundColor: "white",
                  borderRadius: 16,
                  padding: 16
                }}
              >
                <Text style={{ fontSize: 16, fontWeight: "700", textAlign: "center" }}>
                  Select Year
                </Text>

                <FlatList
                  data={years}
                  keyExtractor={(item) => item}
                  style={{ maxHeight: 250 }}
                  renderItem={({ item }) => (
                    <Pressable
                      onPress={() => {
                        setYear(item);
                        setYearPickerVisible(false);
                      }}
                      style={{ paddingVertical: 10 }}
                    >
                      <Text style={{ fontSize: 16 }}>{item}</Text>
                    </Pressable>
                  )}
                />

                <Pressable
                  onPress={() => setYearPickerVisible(false)}
                  style={{ marginTop: 12, alignSelf: "center" }}
                >
                  <Text style={{ fontSize: 16, color: "#555" }}>Close</Text>
                </Pressable>
              </View>
            </View>
          </Modal>

          <View style={rateStyles.formHeadingRow}>
            <Text style={rateStyles.sectionLabel}>Categories and costs</Text>
          </View>

          <Pressable
            onPress={() => {
              setIsAddingCategory(true);
              setErrors("");
            }}
            style={rateStyles.addRow}
          >
            <View style={rateStyles.addIconCircle}>
              <Text style={rateStyles.addIconText}>+</Text>
            </View>
            <Text style={rateStyles.addText}>Add a category</Text>
          </Pressable>

          {isAddingCategory && (
            <View>
              <View style={rateStyles.divider} />
              <View style={rateStyles.rateRow}>
                <Pressable onPress={() => setIsAddingCategory(false)}>
                  <View style={[rateStyles.minusIcon, { backgroundColor: "#555" }]} />
                </Pressable>

                <TextInput
                  style={rateStyles.categoryInput}
                  placeholder="Enter category name"
                  placeholderTextColor="#9CA3AF"
                  value={newCategoryName}
                  onChangeText={setNewCategoryName}
                  onSubmitEditing={addNewCategory}
                />

                <CurrencyInput
                  label=""
                  value={newCategoryRate}
                  onChangeText={setNewCategoryRate}
                  style={{ width: 90 }}
                />
              </View>
            </View>
          )}

          <View style={rateStyles.divider} />

          {categories.map((c, idx) => (
            <View key={c.id}>
              <View style={rateStyles.rateRow}>
                <Pressable onPress={() => deleteCategory(c.id)}>
                  <View style={rateStyles.minusIcon} />
                </Pressable>

                <Text style={rateStyles.rateRowText}>{c.name}</Text>

                <CurrencyInput
                  label=""
                  value={c.rate}
                  onChangeText={(val) => updateCategoryRate(c.id, val)}
                  style={{ width: 90 }}
                />
              </View>

              {idx < categories.length - 1 && <View style={rateStyles.divider} />}
            </View>
          ))}

          <Pressable onPress={handleSave} style={rateStyles.formSaveButton}>
            <Text style={rateStyles.formSaveText}>Save</Text>
          </Pressable>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}
