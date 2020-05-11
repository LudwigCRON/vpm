
module toggle_resync #(
	parameter DEPTH = 2 // number of DFF (MTBF)
) (
	// clock signals
	input  wire clk,
	// reset signals
	input  wire rstb,
	// signal transfer
	input  wire sig,
	output wire sig_r
);

reg i;

always @(posedge clk or negedge rstb)
begin: toggle
    if (!rstb)
        i <= 1'b0;
    else
        i <= (sig) ? ~i : i;
end

buf copy (sig_r, i);

endmodule