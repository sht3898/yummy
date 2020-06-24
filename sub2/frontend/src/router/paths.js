export default [
  {
    path: "",
    view: "Home",
    name: "home"
  },
  {
    path: "/planner/create",
    view: "CreatePlan",
    name: "createplan"
  },
  {
    path: "/planner/detail/:id",
    view: "DetailPlan",
    name: "detailplan"
  },
  {
    path: "/detail",
    view: "Detail",
    name: "detail"
  },
  {
    path: "/auth/verify",
    view: "UserVerify",
    name: "verify",
  },
  {
    path: "/auth/userinfo",
    view: "UserInfo",
    name: "userinfo",
  },
  {
    path: "/store/list",
    view: "StoreList",
    name: "storelist",
  },
  {
    path: "/store/detail",
    view: "StoreDetail",
    name: "storedetail",
  },
  {
    path: "/spot/detail",
    view: "SpotDetail",
    name: "spotdetail",
  },
  {
    path: "/planlist",
    view: "PlannerList",
    name: "plannerlist",
  },
  {
    path: "/planlistdetail",
    view: "PlannerListDetail",
    name: "plannerlistdetail",
  },
  
];
