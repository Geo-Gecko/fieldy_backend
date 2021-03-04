"""
# import pandas as pd
df = pd.read_csv('')
df_2019 = df[~df.Year.isin([2020])]
"""

# check on 2020_exists
# TODO: updating indicator starts. DONE ✔✔✔✔✔

"""
SCRIPT FOR SAVING GRIDS
let gridFeatures = grid.toGeoJSON()
gridFeatures.features.forEach(ft_ => {
return axiosInstance
    .post('/layers/gridlayers/', ft_)
    .then(response => {
        console.log("Layer saved", response)
    })
    .catch(error => {
    console.log(error)
    });
})
"""

"""
// SCRIPT TO SEND KATOR CALCNS
Object.keys(storeData).forEach(kator => {
    Object.keys(storeData[kator]).forEach(cropType => {
    storeData[kator][cropType]["indicator"] = kator
    storeData[kator][cropType]["crop_type"] = cropType
        return axiosInstance
            .post(
            '/layers/indicatorcalculations/',
            storeData[kator][cropType]
            )
            .then(response => {
                console.log("Kator Calc saved", response)
            })
            .catch(error => {
            console.log(error)
            });
    })
})
"""


"""
# import time
# import json

with open("jan_feb_data.json", "+r") as json_file:
    json_file = json.loads(json_file.read())
    unread_ = 0
    initial_ = 0
    for row_ in json_file:
        # 6ec3f626-cd1a-4994-9177-3eb82a0beb0f
        field_ndvi_obj = ArrayedFieldIndicators.objects.filter(
            field_id=row_["field_id"], indicator=row_["indicator"]
        )
        if field_ndvi_obj:
            row_["user_id"] = field_ndvi_obj.first().user_id
            serializer = self.serializer_class(
                field_ndvi_obj[0], data=row_
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            initial_ += 1
            print(f"Added {initial_} fields")
            # time.sleep(1)
        else:
            unread_ += 1
            print(f"Skipped {unread_} fields")
    print(f"done with all {initial_} fields")
"""

"""js scripts"""
"""MORINGA CONNECT"""
# axiosInstance({
#   url: `/layers/fieldindicators/`,
#   method: "GET",
#   data: ""
# })
#   .then(async response => {
#     fieldindicatos.forEach(feature_ => {
#       feature_.year = parseInt(feature_.year)
#       if (feature_.year === 2020) {
#         // let existing_ft_data = response.data.find(ft_data => {
#         //   if (feature_.field_id === ft_data.field_id && ft_data.year === 2020) {
#         //     return ft_data
#         //   }
#         //   return null
#         // })
#         let ft_data_2019 = fieldindicatos.find(ft_ => {
#           if (ft_.year === 2019 && ft_.field_id === feature_.field_id) {
#             return ft_
#           }
#           return null
#         })
#         // let missing_months = [/*"september",*/ "october", "november"]
#         // missing_months.forEach(month_ => {
#         //   feature_.field_rainfall[month_] = ""
#         //   feature_.field_ndvi[month_] = ""
#         //   feature_.field_ndwi[month_] = ""
#         //   feature_.field_temperature[month_] = ""
#         // })
#         // console.log(feature_, "mmmmmm", ft_data_2019)
#         feature_.field_rainfall.december = ft_data_2019.field_rainfall.december
#         feature_.field_ndvi.december = ft_data_2019.field_ndvi.december
#         feature_.field_ndwi.december = ft_data_2019.field_ndwi.december
#         feature_.field_temperature.december = ft_data_2019.field_temperature.december
#         // this.props.dispatch(getcreateputGraphData(
#         //  feature_, 'POST', ""
#         // ))
#         // if (!existing_ft_data) {
#         //   count += 1
#         // }
#       }
#     })
#     // console.log(fieldindicatos)
#     // TESTING THAT WE HAVE THE RIGHT DATA
#     // this.props.dispatch(getcreateputGraphData(
#     //  fieldindicatos[0], 'POST', ""
#     // ))
#   })
# // this.props.postPolygonLayer(farmAfrica.features[0])


"""As of 4th DEECEMBER"""
    # // console.log(fields_)
    # let count = 0
    # fields_.features.forEach(feature => {
    #   feature.properties.field_attributes = {}
    #   feature.properties.user_id = ""
    #   feature.properties.field_attributes.CropType = "Coffee"
    #   let keys_ = Object.keys(feature.properties)
    #   keys_.forEach(key => {
    #     if (!["user_id", "field_attributes", "field_id"].includes(key)) {
    #       if (feature.properties[key] === null) {
    #         feature.properties[key] = ""
    #       }
    #       // croptype is below
    #       if (key === "Select Value chain") {
    #         // console.log("count")
    #         feature.properties.field_attributes.CropType = feature.properties[key]
    #         delete feature.properties[key]
    #       } else {
    #         feature.properties.field_attributes[key] =
    #          feature.properties[key]
    #         delete feature.properties[key]
    #       }
    #     }
    #   })
    #   let already_there = leafletGeoJSON.features.find(ft_ => {
    #     if (ft_.properties.field_id === feature.properties.field_id) {
    #       return ft_
    #     }
    #     return null
    #   })
    #   if (!already_there){
    #     count += 1
    #     // this.props.postPolygonLayer(feature)
    #   }
    # })

"""UPDATING INDICATOR DATA"""

#     // console.log(count)
#     axiosInstance({
#       url: `/layers/fieldindicators/`,
#       method: "GET",
#       data: ""
#   })
#       .then(async response => {
#         // console.log(response.data, fieldindicators)
        # count = 0
        # response.data.forEach((piece_, index) => {
        #   let updated_ft_data = fieldindicators.find(ft_data => {
        #     // ft_data.field_id = ft_data.field_id.replace("{", "")
        #     if (piece_.field_id === ft_data.field_id && ft_data.year === 2020) {
        #       return ft_data
        #     }
        #     return null
        #   })
        #   if (updated_ft_data){
        #     count ++;
        #     // WITHOUT STAGGERING____
        #   //   axiosInstance({
        #   //     url: `/layers/fieldindicators/${updated_ft_data.field_id}/`,
        #   //     method: "PUT",
        #   //     data: updated_ft_data
        #   // })
        #   //     .then(response => console.log(response.data))
        #   // WITH STAGGERING_______________________________________
        #     setTimeout(function(){
        #       // console.log(count)
        #   //   axiosInstance({
        #   //     url: `/layers/fieldindicators/${updated_ft_data.field_id}/`,
        #   //     method: "PUT",
        #   //     data: updated_ft_data
        #   // })
        #   //     .then(response => console.log(response.data))
        #     }, index * 250)
        #   }
        # })
#         console.log(count)
    

#         })
