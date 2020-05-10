
module adc_sar #(
    parameter WIDTH = 4'd10
) (
    input   wire                clk,
    input   wire                rstb,
    input   wire                enable,
    input   wire                ms_cmp,
    input   wire                ms_rdy,
    output  wire    [WIDTH-1:0] ms_dac,
    output  wire    [WIDTH-1:0] adata
);

endmodule