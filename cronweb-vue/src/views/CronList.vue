<template>
    <div class="home">
        <div class="action">
            <el-button type="success" @click="showAdd">新增任务</el-button>
        </div>
        <el-table
                :data="tableData"
                border
                stripe
                style="width: 100%">
            <el-table-column width="160" prop="name" label="任务名"></el-table-column>
            <el-table-column prop="cmd" label="Shell命令"></el-table-column>
            <el-table-column width="150" prop="run_time" label="执行时间"></el-table-column>
            <el-table-column width="140" prop="second" label="执行毫秒数 (s)"></el-table-column>
            <el-table-column width="180" prop="next_time" label="下次执行时间"></el-table-column>
            <el-table-column width="100" prop="status" label="状态">
                <template #default="scope">
                    <el-tag effect="dark" :type="scope.row.status === 'Running' ? 'success' : 'danger'"
                            disable-transitions>
                        {{scope.row.status}}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column fixed="right" label="操作">
                <template #default="scope">

                    <el-button v-if="scope.row.status==='Running'" @click="stopTask(scope.row.id)" type="danger"
                               size="small">停止
                    </el-button>
                    <el-button v-if="scope.row.status==='Stopped'" @click="startTask(scope.row.id)" type="success"
                               size="small">启动
                    </el-button>
                    <el-button type="info" @click="deleteTask(scope.row.id)" size="small">删除</el-button>
                    <el-button type="primary" @click="showInfo(scope.row.id)" size="small">详细信息</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog title="新增任务" v-model="dialogFormVisible" width="40%">
            <el-form :model="form" style="font-weight: bold;" size="normal" label-width="120px">
                <el-form-item label="任务名称">
                    <el-input v-model="form.name" style="width: 80%;" placeholder="请输入任务名称"></el-input>
                </el-form-item>
                <el-form-item label="执行时间">
                    <el-radio-group style="width: 100%;padding-bottom: 10px" v-model="modelCheck">
                        <el-radio :label="1">使用Cron表达式</el-radio>
                        <el-radio :label="2">使用毫秒数</el-radio>
                    </el-radio-group>

                    <el-input v-if="modelCheck === 1" v-model="form.run_time" placeholder="输入Cron表达式"
                              style="width: 80%;"></el-input>
                    <el-input-number v-if="modelCheck===2" v-model="form.second"></el-input-number>
                </el-form-item>
                <el-form-item label="执行命令">
                    <el-input type="textarea" :autosize="{ minRows: 3, maxRows: 5}"
                              placeholder="请输入内容" v-model="form.cmd"></el-input>
                </el-form-item>
                <el-form-item label="创建后立即运行">
                    <el-switch v-model="form.status" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                </el-form-item>

            </el-form>
            <template #footer>
    <span class="dialog-footer">
      <el-button @click="dialogFormVisible = false">取 消</el-button>
      <el-button type="primary" @click="addTask">确 定</el-button>
    </span>
            </template>
        </el-dialog>


        <el-dialog title="详细信息" v-model="infoDialog">
            <p>任务名: {{infoData.name}}</p>
            <p>下次执行时间: {{infoData.next_time}}</p>
            <p>执行命令: {{infoData.cmd}}</p>
            <p v-text="JSON.stringify(infoData.stdout)"></p>
        </el-dialog>
    </div>

</template>

<script>
    // @ is an alias to /src
    import request from "../utils/request";

    export default {
        name: 'CronList',
        components: {},
        data() {
            return {
                dialogFormVisible: false,
                form: {
                    status: true
                },
                tableData: [],
                modelCheck: 1,
                infoDialog: false,
                infoData: null,
            }
        },
        methods: {
            load() {
                request.get("/list", {}).then(resp => {
                    this.tableData = resp.data;
                }).catch(err => {
                    alert(err)
                })
            },
            showAdd() {
                this.form = {status: true};
                this.dialogFormVisible = true;
            },
            addTask() {
                //新增
                request.post("/add", this.form).then(res => {
                    this.$message.success({
                        message: '新增任务成功',
                        type: 'success'
                    });
                    this.load()
                    this.dialogFormVisible = false

                }).catch(err => {
                    this.$message.error(err.response.data.detail);
                })


            },
            startTask(task_id) {
                this.$confirm('确定启动任务吗, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    request.get("/start", {
                        params: {
                            "task_id": task_id
                        }
                    }).then(res => {
                        this.$message({
                            type: 'success',
                            message: '启动成功!'
                        });
                        // 刷新
                        this.load()
                    }).catch(err => {
                        this.$message.error(err.response.data.detail);
                    })
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消启动'
                    });
                });
            },
            stopTask(task_id) {

                this.$confirm('确定停止任务吗, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    request.get("/stop", {
                        params: {
                            "task_id": task_id
                        }
                    }).then(res => {
                        this.$message({
                            type: 'success',
                            message: '停止成功!'
                        });
                        // 刷新
                        this.load()
                    }).catch(err => {
                        this.$message.error(err.response.data.detail);
                    })
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消停止任务'
                    });
                });
            },
            deleteTask(task_id) {

                this.$confirm('此操作将永久删除, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    request.get("/del", {
                        params: {
                            "task_id": task_id
                        }
                    }).then(res => {
                        this.$message({
                            type: 'success',
                            message: '删除成功!'
                        });
                        // 刷新
                        this.load()
                    }).catch(err => {
                        this.$message.error(err.response.data.detail);
                    })
                }).catch(err => {
                    this.$message({
                        type: "info",
                        message: "已取消删除"
                    });
                });
            },
            showInfo(task_id) {
                request.get("/log/" + task_id).then(res => {
                    // 刷新
                    this.infoDialog = true
                    this.infoData = res.data
                }).catch(err => {
                    this.$message.error(err.response.data.detail);
                })

            }

        }, mounted() {
            this.load()
        }
    }
</script>
<style scoped>
    .home {
        padding: 10px;
    }

    .action {
        margin: 10px 0;
    }
</style>
