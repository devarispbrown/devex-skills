// Hook registration sample. Declares the hook contract it implements.
export default {
  hook: "on_task_complete",
  args_schema: ["task_id", "status"],
  handle: async (ctx) => ctx.log(`task ${ctx.task_id} ${ctx.status}`),
};
