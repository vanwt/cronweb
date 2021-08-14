<template>

    <div class="nav">
        <div class="logo"><h2>Cron管理</h2></div>
        <div class="search"></div>
        <div class="user">
            <el-dropdown>
                <span class="el-dropdown-link">
                    管理员
                    <i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item>重启系统</el-dropdown-item>
                        <el-dropdown-item>退出</el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Header"
    }
</script>

<style scoped>
    .nav {
        height: 50px;
        line-height: 50px;
        border-bottom: 1px solid #ccc;
        display: flex;
        padding-left: 30px;
        font-weight: bold;
        color: dodgerblue;
    }

    .logo {
        width: 200px;
        color: black;
    }

    .search {
        flex: 1;
    }

    .user {
        width: 100px;
    }
</style>