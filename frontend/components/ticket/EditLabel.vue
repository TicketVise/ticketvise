<template>
    <div class="flex flex-column items-start">
        <h4 class="font-semibold text-gray-800 mb-2">Labels</h4>
        <div class="flex flex-wrap mb-2">
            <chip class="m-1" v-for="(label, index) in ticket.labels" :key="label.id" :background="label.color">
                {{label.name}}
                <a class="fa fa-close" @click="deleteEvent(index)"></a>
            </chip>
        </div>

        <label-dropdown v-bind:value="value" :values="unused_labels" v-on:input="submit" class="w-full"/>
    </div>

</template>

<script>
    import Chip from "../elements/chip/Chip";
    import LabelDropdown from "../elements/dropdown/LabelDropdown";
    import axios from "axios";

    export default {
        components: {LabelDropdown, Chip},
        name: "EditLabel",
        props: ["ticket"],
        data() {
            return {
                value: null,
                inbox_labels: null,
                labels: []
            }
        },
        mounted() {
            axios.get("/api/inboxes/" + this.ticket.inbox + "/labels").then(response => {
                this.inbox_labels = response.data;
            });
        },
        methods: {
            submit(label) {
                this.value = label
                this.labels = [this.value.id];

                let dictionary = this.ticket.labels;
                for (let key in dictionary) {
                    this.labels.push(dictionary[key].id)
                }

                axios.defaults.xsrfCookieName = 'csrftoken';
                axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

                axios.put("/api" + window.location.pathname + "/labels", {"labels": this.labels})
                    .then(response => {
                        this.ticket.labels.push(this.value)
                        this.value = null
                    });
            },
            deleteEvent: function (index) {
                this.ticket.labels.splice(index, 1);

                let dictionary = this.ticket.labels;
                for (let key in dictionary) {
                    this.labels.push(dictionary[key].id)
                }

                let formData = new FormData();
                formData.append("labels", this.labels);

                axios.defaults.xsrfCookieName = 'csrftoken';
                axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

                axios.put("/api" + window.location.pathname + "/labels", {"labels": this.labels})
                    .then(_ => {
                    });
            }
        },
        computed: {
            unused_labels: function () {
                if (!this.inbox_labels) {
                    return []
                }

                const ticket_label_ids = this.ticket.labels.map(label => label.id)

                return this.inbox_labels.filter(label => !ticket_label_ids.includes(label.id))
            }
        }
    }
</script>

<style scoped>

</style>