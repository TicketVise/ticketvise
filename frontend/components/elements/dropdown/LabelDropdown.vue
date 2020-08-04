<template>
    <div class="inline-block relative w-64">
        <select v-on:input="updateValue($event.target.value)"
                class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline">
            <option>Add label</option>
            <option :value="item.id" v-for="item in values" :key="item.id">{{item.name}}</option>
        </select>
    </div>
</template>

<script>
    export default {
        name: "Dropdown",
        props: ["values", "value"],
        methods: {
            updateValue: function (value) {
                const selected = this.values.filter(label => label.id === parseInt(value))[0];
                this.$emit('input', selected)
            }
        }
    }
</script>

<style scoped>

</style>
