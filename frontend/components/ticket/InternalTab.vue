<template>
    <div class="flex flex-column flex-wrap w-full">
        <div class="mt-3 w-full">
            <div class="mb-3" v-if="comments.length === 0">
                It seems like there are no messages yet, be the first!
            </div>
            <comment v-for="comment in comments" :key="comment.id" :comment="comment" :ticket="ticket"/>
        </div>

        <div class="flex w-full">
            <avatar :source="user.avatar_url" size="w-12 h-12 m-3"/>
            <div class="flex-grow w-full">
                <card outlined class="mb-2 w-full">
                    <mention :ticket="ticket" :users="staff">
                        <editor ref="commentEditor" initialEditType="wysiwyg" previewStyle="tab"/>
                    </mention>
                </card>
                <span class="shadow-sm rounded-md">
                    <submit-button @click="submitComment" text="Comment"></submit-button>
                </span>
            </div>
        </div>
    </div>
</template>

<script>
    import Comment from "./Comment";
    import Avatar from "../elements/Avatar";
    import axios from "axios";
    import '@toast-ui/editor/dist/toastui-editor-viewer.css';
    import 'codemirror/lib/codemirror.css';
    import VueTribute from 'vue-tribute';

    import '@toast-ui/editor/dist/toastui-editor.css';
    import {Editor, Viewer} from '@toast-ui/vue-editor';
    import Card from "../elements/card/Card";
    import Mention from "../elements/mention/Mention";
    import SubmitButton from "../elements/buttons/SubmitButton";

    export default {
        components: {
            SubmitButton,
            Mention,
            Avatar,
            Comment,
            Viewer,
            editor: Editor,
            VueTribute,
            Card
        },
        props: {
            ticket: {
                type: Object,
                required: true
            },
            comments: {
                required: true,
                default: []
            },
            user: {
                type: Object,
                required: true
            },
            staff: {
                required: true,
                default: []
            }
        },
        methods: {
            submitComment() {
                let content = this.$refs.commentEditor.invoke('getMarkdown');
                this.$refs.commentEditor.invoke('setMarkdown', '');

                let formData = new FormData();
                formData.append("content", content);

                axios.defaults.xsrfCookieName = 'csrftoken';
                axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

                axios.post("/api" + window.location.pathname + "/comments/post", formData)
                    .then(() => {
                        this.$emit("post", true)
                    })
            },
        },
    }
</script>

<style scoped>

</style>