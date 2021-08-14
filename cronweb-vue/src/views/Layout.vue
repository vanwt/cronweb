<template>
    <div>
        <Header/>
        <!--主体-->

        <!--内容区域-->
        <el-row :gutter="20">
            <el-col :span="18" :offset="3">
                <cron-list/>
            </el-col>
        </el-row>

    </div>
</template>

<script>
    import Header from "../components/Header";
    import CronList from "./CronList";

    export default {
        name: "Layout",
        components: {
            Header,
            CronList
        },

    }
</script>

<style scoped>

</style>