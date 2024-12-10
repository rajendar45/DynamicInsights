 var app = angular.module('insightsApp', []);
        app.controller('InsightsController', function($scope, $http) {
            $scope.results = [];
            $scope.search = function() {
                $http.get('http://localhost:8080/generate_insights?question=' + $scope.query)
                    .then(function(response) {
                        $scope.results = response.data;
                    });
            };

            $scope.exportToCSV = function() {
                let csvContent = "data:text/csv;charset=utf-8,";
                csvContent += "Key,Value\n";
                $scope.results.forEach(function(result) {
                    for (let key in result) {
                        if (result.hasOwnProperty(key)) {
                            let row = key + "," + result[key];
                            csvContent += row + "\n";
                        }
                    }
                });

                var encodedUri = encodeURI(csvContent);
                var link = document.createElement("a");
                link.setAttribute("href", encodedUri);
                link.setAttribute("download", "results.csv");
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            };
        });
       