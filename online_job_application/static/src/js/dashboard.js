/**@odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

const actionRegistry = registry.category("actions");

class JobDashboard extends Component {
    setup() {
        this.state = useState({
            totalCandidates: 0,
            totalJobs: 0,
            publishedJobs: 0,
            unpublishedJobs: 0,
            jobData: [],
        });

        onWillStart(async () => {
            try{
                const dashboardData = await rpc('/dashboard_data', {})
                this.state = {
                    ...this.state,
                    totalCandidates: dashboardData.total_candidates,
                    totalJobs: dashboardData.total_jobs,
                    publishedJobs: dashboardData.published_jobs,
                    unpublishedJobs: dashboardData.unpublished_jobs,
                    jobData: dashboardData.job_position_table,
                };
            } catch (error) {
                console.error("Failed to fetch dashboard data:", error);
            }
        });
    }
}

JobDashboard.template = "online_job_application.JobDashboard";

actionRegistry.add("job_dashboard_tag", JobDashboard);
export default JobDashboard;
